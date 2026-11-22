# Yerel kurulum

## Gereksinimler

- Docker Desktop ve Docker Compose v2
- Model indirmek için internet bağlantısı
- LLM çalıştırmaya yetecek RAM veya desteklenen GPU

## Başlatma

Depo kök dizininde:

```bash
docker compose up --build -d
```

`ollama-init` servisi ilk açılışta iki modeli otomatik indirir. İndirme tamamlanınca:
- Web arayüzü: http://localhost:3000
- Swagger: http://localhost:8080/swagger
- API health: http://localhost:8080/health
- AI health: http://localhost:8000/health

## Hızlı deneme

```bash
curl -X POST http://localhost:8080/api/knowledge -H "Content-Type: application/json" -d '{"title":"VPN Rehberi","content":"VPN bağlantısı için kurum hesabınızla oturum açın, VPN istemcisini çalıştırın ve kurum sunucu adresini girin. Ardından çok faktörlü doğrulamayı tamamlayın."}'
curl -X POST http://localhost:8080/api/assistant/ask -H "Content-Type: application/json" -d '{"question":"VPN bağlantısı nasıl kurulur?"}'
curl -X POST http://localhost:8080/api/tickets -H "Content-Type: application/json" -d '{"title":"VPN bağlantı sorunu","description":"Ofis dışından VPN bağlantısı kuramıyorum."}'
```

## Test

```bash
cd ai-service
python -m pip install -r requirements.txt pytest
pytest -q
```

İlk açılışta API PostgreSQL tablolarını demo amaçlı `EnsureCreated` ile oluşturur. Canlı sistemde migration tabanlı şema yönetimine geçilmelidir.
