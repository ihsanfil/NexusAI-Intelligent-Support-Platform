# NexusAI – Akıllı Destek ve Talep Yönetim Platformu

NexusAI; kurumsal destek taleplerini yönetmek, yerel LLM ile sınıflandırmak ve bilgi bankasından RAG tabanlı yanıt önerileri üretmek için geliştirilen çok servisli bir uygulamadır.

## Teknoloji yığını

- **Backend:** C#, .NET 8, ASP.NET Core Web API, EF Core
- **Mimari:** N-Tier / katmanlı mimari, Domain ve Infrastructure ayrımı
- **Frontend:** React, Vite, Nginx
- **AI:** Python, FastAPI, Pydantic, Uvicorn
- **LLM:** Ollama, yerel model çalıştırma
- **RAG:** chunking, embeddings, cosine similarity, semantic retrieval, kaynaklı yanıt üretimi
- **Veri:** PostgreSQL, Redis; pgvector tabanlı PostgreSQL imajı
- **Dağıtım:** Docker, Docker Compose, Nginx
- **Kalite:** Swagger / OpenAPI, sağlık kontrolü, GitHub Actions CI, pytest

## Özellikler

- Talep oluşturma, sayfalı listeleme, detay görüntüleme ve durum güncelleme
- Ollama üzerinden talep kategorisi, önceliği ve yanıt önerisi
- Bilgi dokümanı ekleme ve listeleme
- Dokümanları parçalara ayırma ve embedding vektörleri üretme
- Cosine similarity ile anlamsal arama ve kaynaklı RAG yanıtı
- PostgreSQL üzerinde taleplerin ve doküman metadata bilgilerinin kalıcı saklanması
- Redis üzerinde doküman parçaları ve embedding vektörleri
- React yönetim ekranı ve Nginx reverse proxy

## Mimari

```text
React UI -> Nginx -> ASP.NET Core API -> PostgreSQL
                         |-> Redis
                         |-> Python FastAPI -> Ollama (LLM + Embeddings)
```

## Çalıştırma

Docker Desktop / Docker Engine ve Compose v2 gereklidir.

```bash
docker compose up --build -d
docker compose exec ollama ollama pull llama3.2:3b
docker compose exec ollama ollama pull nomic-embed-text
```

Model indirmeleri tamamlandıktan sonra:

- Web arayüzü: http://localhost:3000
- API Swagger: http://localhost:8080/swagger
- API sağlık: http://localhost:8080/health
- AI servis sağlık: http://localhost:8000/health
- Ollama: http://localhost:11434

Detaylı kurulum ve örnek istekler için [Yerel Kurulum](docs/LOCAL-SETUP.md), mimari kararlar için [Mimari](docs/ARCHITECTURE.md) dokümanına bakın.

## RAG akışı

1. Doküman PostgreSQL'e metadata olarak kaydedilir.
2. AI servisi içeriği yaklaşık 900 karakterlik ve 120 karakter örtüşmeli parçalara böler.
3. Her parça `nomic-embed-text` ile vektörleştirilir ve Redis'e yazılır.
4. Soru vektörü çıkarılır, cosine similarity ile en yakın beş parça seçilir.
5. Seçilen parçalar kaynak başlıklarıyla LLM'e gönderilir.

## Testler

```bash
cd ai-service
pip install -r requirements.txt pytest
pytest -q
```

GitHub Actions, .NET derlemesini, Python testlerini ve React üretim derlemesini kontrol eder.

## Kapsam ve canlıya geçiş notları

Bu depo çalışan bir geliştirme/demo temelidir; üretim ortamına hazır olduğu iddia edilmemektedir. Redis anahtarlarının toplu taranması büyük veri hacimleri için uygun değildir. Üretim öncesinde JWT/OIDC ve rol bazlı yetkilendirme, tenant izolasyonu, dosya yükleme/indeksleme kuyruğu, doküman silme ve yeniden indeksleme, pgvector veya Redis Vector Search indeksleri, migration tabanlı şema yönetimi, secret manager, rate limiting, audit log, izleme ve yedekleme eklenmelidir.

Fine-tuning, 4-bit/8-bit quantization ve vLLM olası model eğitimi/servisleme seçenekleridir; mevcut compose akışı otomatik fine-tuning gerçekleştirmez. Ollama modelleri kendi paket quantization biçimleriyle sunulur. Geliştirme parolaları yalnızca yerel kullanım içindir.

## Anahtar kelimeler

ASP.NET Core, .NET 8, C#, Web API, EF Core, N-Tier Architecture, Clean Architecture, React, Python, FastAPI, AI Engineering, Artificial Intelligence, Machine Learning, NLP, LLM, Large Language Models, RAG, Retrieval-Augmented Generation, Prompt Engineering, Embeddings, Chunking, Vector Search, Semantic Search, Fine-Tuning, Quantization, 4-bit Quantization, 8-bit Quantization, Ollama, vLLM, PostgreSQL, pgvector, Redis, Docker, Docker Compose, Nginx, Uvicorn, REST API, Swagger, OpenAPI, CI/CD, GitHub Actions, On-Premise AI, Local LLM, Enterprise AI, Ticket Management.
