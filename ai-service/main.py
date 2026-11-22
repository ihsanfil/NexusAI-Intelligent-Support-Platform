import json
import math
import os
import re
import uuid
from typing import List

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from redis.asyncio import Redis

app = FastAPI(title="NexusAI AI Servisi", version="1.0.0")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
redis_client: Redis | None = None
DOC_PREFIX = "nexusai:knowledge:"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 120


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
        redis_client = None


@app.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.aclose()


@app.get("/health")
async def health():
    redis_ok = False
    if redis_client:
        try:
            redis_ok = bool(await redis_client.ping())
        except Exception:
            pass
    return {"durum": "çalışıyor", "servis": "NexusAI AI", "redis": redis_ok}


async def ollama_post(path: str, payload: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{OLLAMA_URL}{path}", json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="Ollama yanıt vermedi. Model ve servis durumunu kontrol edin.") from exc


async def ollama_generate(prompt: str) -> str:
    result = await ollama_post("/api/generate", {
        "model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
        "options": {"temperature": 0.2}
    })
    return result.get("response", "").strip()


async def embed(text: str) -> list[float]:
    result = await ollama_post("/api/embeddings", {"model": EMBED_MODEL, "prompt": text})
    vector = result.get("embedding")
    if not vector:
        raise HTTPException(status_code=503, detail=f"Embedding modeli ({EMBED_MODEL}) hazır değil.")
    return vector


def split_into_chunks(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    chunks, start = [], 0
    while start < len(normalized):
        end = min(len(normalized), start + CHUNK_SIZE)
        chunks.append(normalized[start:end])
        if end == len(normalized):
            break
        start = end - CHUNK_OVERLAP
    return chunks


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    prompt = (
        "Kurumsal destek uzmanı olarak aşağıdaki talebi Türkçe değerlendir. "
        "Yalnızca JSON döndür: category, priority, answer. priority düşük, orta veya yüksek olsun. "
        "Kısa, uygulanabilir ve bilgi uydurmayan yanıt ver.\n"
        f"Talep: {request.text}"
    )
    raw = await ollama_generate(prompt)
    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        data = json.loads(match.group(0) if match else raw)
        priority = str(data.get("priority", "orta")).lower()
        if priority not in {"düşük", "orta", "yüksek"}:
            priority = "orta"
        return AnalyzeResponse(
            category=str(data.get("category", "Genel destek"))[:100],
            priority=priority,
            answer=str(data.get("answer", "Talebiniz incelenmek üzere kaydedildi."))[:2000],
            sources=[]
        )
    except (ValueError, TypeError):
        return AnalyzeResponse(category="Genel destek", priority="orta",
                               answer=raw[:2000] or "Talep incelenmek üzere kaydedildi.", sources=[])


@app.post("/knowledge")
async def add_knowledge(request: KnowledgeRequest):
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Bilgi bankası için Redis bağlantısı gerekli.")
    document_id = str(uuid.uuid4())
    chunks = split_into_chunks(request.content)
    for index, chunk in enumerate(chunks):
        vector = await embed(chunk)
        await redis_client.hset(
            f"{DOC_PREFIX}{document_id}:{index}",
            mapping={"document_id": document_id, "title": request.title,
                     "chunk": chunk, "embedding": json.dumps(vector), "chunk_index": index}
        )
    await redis_client.hset(f"{DOC_PREFIX}{document_id}:meta",
                            mapping={"title": request.title, "chunk_count": len(chunks)})
    return {"id": document_id, "title": request.title, "parca_sayisi": len(chunks), "durum": "indekslendi"}


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Bilgi bankası için Redis bağlantısı gerekli.")
    question_vector = await embed(request.question)
    keys = await redis_client.keys(DOC_PREFIX + "*")
    ranked = []
    for key in keys:
        if key.endswith(":meta"):
            continue
        data = await redis_client.hgetall(key)
        try:
            vector = json.loads(data.get("embedding", "[]"))
        except json.JSONDecodeError:
            continue
        score = cosine_similarity(question_vector, vector)
        if score > 0.15:
            ranked.append((score, data.get("title", "İsimsiz doküman"), data.get("chunk", "")))
    ranked.sort(key=lambda item: item[0], reverse=True)
    selected = ranked[:5]
    if not selected:
        return AskResponse(answer="Bilgi bankasında sorunuzla anlamsal olarak eşleşen bir kaynak bulamadım.", sources=[])
    context = "\n\n".join(f"Kaynak: {title}\nİçerik: {chunk}" for _, title, chunk in selected)
    prompt = (
        "Yalnızca aşağıdaki kaynaklarda bulunan bilgilere dayanarak Türkçe yanıt ver. "
        "Kaynaklarda cevap yoksa bunu açıkça söyle. Bilgi uydurma.\n\n"
        f"Kaynaklar:\n{context}\n\nSoru: {request.question}"
    )
    answer = await ollama_generate(prompt)
    return AskResponse(answer=answer[:5000], sources=list(dict.fromkeys(title for _, title, _ in selected)))
