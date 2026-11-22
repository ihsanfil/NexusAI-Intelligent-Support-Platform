import os
from typing import List

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="NexusAI AI Servisi", version="0.1.0")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=3, max_length=12000)

class AnalyzeResponse(BaseModel):
    category: str
    priority: str
    answer: str
    sources: List[str]

@app.get("/health")
async def health():
    return {"durum": "çalışıyor", "servis": "NexusAI AI"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    # Model yanıtı alınamazsa kullanıcıya anlaşılır bir servis hatası döndürülür.
    prompt = (
        "Aşağıdaki destek talebini Türkçe değerlendir. JSON olarak category, priority, answer alanlarını döndür. "
        "priority yalnızca düşük, orta veya yüksek olsun. Yanıtı kısa ve uygulanabilir tut.\n\n"
        f"Talep: {request.text}"
    )
    try:
        async with httpx.AsyncClient(timeout=75) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
                      "format": "json"},
            )
            response.raise_for_status()
            payload = response.json()
            import json
            result = json.loads(payload.get("response", "{}"))
            return AnalyzeResponse(
                category=str(result.get("category", "Genel destek")),
                priority=str(result.get("priority", "orta")),
                answer=str(result.get("answer", "Talebiniz incelenmek üzere kaydedilmelidir.")),
                sources=[],
            )
    except (httpx.HTTPError, ValueError, KeyError) as exc:
        raise HTTPException(status_code=503, detail="Yerel LLM yanıt veremedi. Ollama ve model durumunu kontrol edin.") from exc
