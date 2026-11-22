import json
import os
import re
from typing import List

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from redis.asyncio import Redis

app = FastAPI(title="NexusAI AI Servisi", version="0.2.0")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
redis_client: Redis | None = None
# Basit geliştirme ortamında dokümanlar Redis'e yazılır; servis yeniden başlasa da kaybolmaz.
DOC_PREFIX = "nexusai:knowledge:"


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=3, max_length=12000)


class AnalyzeResponse(BaseModel):
    category: str
    priority: str
    answer: str
    sources: List[str]


class KnowledgeRequest(BaseModel):
    title: str = Field(min_length=2, max_length=300)
    content: str = Field(min_length=20, max_length=50000)


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=12000)


class AskResponse(BaseModel):
    answer: str
    sources: List[str]


@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        await redis_client.ping()
    except Exception:
        # Redis kapalıysa sağlık kontrolü ve model uç noktaları yine kullanılabilir.
        redis_client = None


@app.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.aclose()


@app.get("/health")
async def health():
    return {"durum": "çalışıyor", "servis": "NexusAI AI", "redis": redis_client is not None}


async def ollama_generate(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=100) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            return response.json().get("response", "")
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="Yerel LLM yanıt vermedi. Ollama ve model durumunu kontrol edin.") from exc


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    prompt = (
        "Bir kurumsal destek uzmanı gibi davran. Aşağıdaki talebi Türkçe değerlendir. "
        "Yalnızca JSON döndür: category, priority, answer. priority düşük, orta veya yüksek olsun. "
        "Yanıt kısa, uygulanabilir ve talepte olmayan bilgi uydurmayan şekilde olsun.\n"
        f"Talep: {request.text}"
    )
    raw = await ollama_generate(prompt)
    try:
        # Bazı modeller JSON etrafına açıklama ekleyebildiği için nesne sınırını ayıklıyoruz.
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        data = json.loads(match.group(0) if match else raw)
        priority = str(data.get("priority", "orta")).lower()
        if priority not in {"düşük", "orta", "yüksek"}:
            priority = "orta"
        return AnalyzeResponse(
            category=str(data.get("category", "Genel destek"))[:100],
            priority=priority,
            answer=str(data.get("answer", "Talebiniz incelenmek üzere kaydedilmelidir."))[:2000],
            sources=[],
        )
    except (ValueError, TypeError):
        return AnalyzeResponse(category="Genel destek", priority="orta",
                               answer=raw[:2000] or "Talep incelenmek üzere kaydedilmelidir.", sources=[])


@app.post("/knowledge")
async def add_knowledge(request: KnowledgeRequest):
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Doküman kaydı için Redis bağlantısı gerekli.")
    import uuid
    document_id = str(uuid.uuid4())
    await redis_client.hset(DOC_PREFIX + document_id, mapping={
        "title": request.title, "content": request.content
    })
    return {"id": document_id, "title": request.title, "durum": "kaydedildi"}


def split_into_chunks(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks


def rank_chunks(question: str, documents: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
    # İlk sürümde Türkçe kelime örtüşmesi kullanılır; embedding tabanlı sıralama sonraki aşamada eklenebilir.
    stop_words = {"ve", "ile", "bir", "bu", "şu", "için", "nasıl", "nedir", "mi", "mı"}
    terms = {w.lower() for w in re.findall(r"[\wçğıöşüÇĞİÖŞÜ]+", question) if len(w) > 2} - stop_words
    ranked = []
    for title, chunk, _ in documents:
        words = set(w.lower() for w in re.findall(r"[\wçğıöşüÇĞİÖŞÜ]+", chunk))
        score = len(terms & words)
        if score:
            ranked.append((score, title, chunk))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [(title, chunk) for _, title, chunk in ranked[:5]]


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Bilgi bankası için Redis bağlantısı gerekli.")
    keys = await redis_client.keys(DOC_PREFIX + "*")
    documents = []
    for key in keys:
        data = await redis_client.hgetall(key)
        for chunk in split_into_chunks(data.get("content", "")):
            documents.append((data.get("title", "İsimsiz doküman"), chunk, key))
    selected = rank_chunks(request.question, documents)
    if not selected:
        return AskResponse(answer="Bilgi bankasında soruyla eşleşen bir içerik bulamadım. İlgili dokümanları ekleyebilirsiniz.", sources=[])
    context = "\n\n".join(f"Kaynak: {title}\nİçerik: {chunk}" for title, chunk in selected)
    prompt = (
        "Yalnızca aşağıdaki kaynaklarda bulunan bilgilere dayanarak Türkçe yanıt ver. "
        "Kaynaklarda cevap yoksa bunu açıkça söyle. Bilgi uydurma.\n\n"
        f"Kaynaklar:\n{context}\n\nSoru: {request.question}"
    )
    answer = await ollama_generate(prompt)
    return AskResponse(answer=answer[:5000], sources=list(dict.fromkeys(title for title, _ in selected)))
