# NexusAI – Akıllı Destek ve Talep Yönetim Platformu

NexusAI, kurumsal destek taleplerini yönetmek, LLM ile sınıflandırmak ve kurum içi bilgi bankasından RAG tabanlı yanıt önerileri üretmek için geliştirilen çok servisli bir uygulamadır.

## Teknoloji yığını

- **Backend:** C#, .NET 8, ASP.NET Core Web API, EF Core
- **Mimari:** N-Tier / katmanlı mimari, Domain ve Infrastructure ayrımı
- **AI:** Python, FastAPI, Pydantic, Uvicorn
- **LLM:** Ollama (yerel model); vLLM uyumlu servis entegrasyonu sonraki genişletme noktasıdır
- **RAG:** doküman parçalama (chunking), anahtar kelime tabanlı ilk retrieval, kaynaklı yanıt üretimi
- **Veri:** PostgreSQL, Redis
- **Dağıtım:** Docker, Docker Compose, Nginx yapılandırması
- **Kalite:** Swagger / OpenAPI, istek doğrulama, sağlık kontrolü

## Özellikler

- Talep oluşturma, sayfalı listeleme, detay görüntüleme ve durum güncelleme
- Ollama üzerinden talep kategorisi, önceliği ve yanıt önerisi
- Bilgi dokümanı ekleme ve listeleme
- Redis üzerinde doküman saklama, chunking ve ilgili parçaları seçerek RAG yanıtı oluşturma
- PostgreSQL üzerinde taleplerin ve doküman kayıtlarının kalıcı saklanması
- Redis ve PostgreSQL sağlık kontrolü

## Mimari

```text
İstemci -> ASP.NET Core API -> PostgreSQL
                         |-> Redis
                         |-> Python FastAPI -> Ollama
Nginx (isteğe bağlı reverse proxy)
```

## Gereksinimler

- Docker Desktop veya Docker Engine + Compose
- İlk model indirme ve yanıt üretimi için internet bağlantısı
- Model çalıştırmak için yeterli RAM/CPU veya desteklenen GPU

## Çalıştırma

Depo kök dizininde:

```bash
docker compose up --build -d
docker compose exec ollama ollama pull llama3.2:3b
```

Servis adresleri:
- API Swagger: http://localhost:8080/swagger
- API sağlık: http://localhost:8080/health
- AI servis sağlık: http://localhost:8000/health
- Ollama: http://localhost:11434

İlk model indirmesi tamamlandıktan sonra API üzerinden talep oluşturabilirsiniz.

## Örnek istekler

Talep oluşturma:

```bash
curl -X POST http://localhost:8080/api/tickets -H "Content-Type: application/json" -d '{"title":"VPN bağlantı sorunu","description":"Ofis dışından VPN bağlantısı kuramıyorum."}'
```

Bilgi dokümanı ekleme:

```bash
curl -X POST http://localhost:8080/api/knowledge -H "Content-Type: application/json" -d '{"title":"VPN Kullanım Rehberi","content":"VPN bağlantısı için önce kurum hesabınızla oturum açın. İstemciyi başlatıp sunucu adresini girin ve çok faktörlü doğrulamayı tamamlayın."}'
```

Bilgi bankasına soru sorma:

```bash
curl -X POST http://localhost:8080/api/assistant/ask -H "Content-Type: application/json" -d '{"question":"VPN bağlantısı nasıl kurulur?"}'
```

## Önemli geliştirme notları

Bu depo çalışan bir geliştirme başlangıç sürümüdür; henüz üretim ortamına hazır bir ürün olarak değerlendirilmemelidir. İlk RAG retrieval yöntemi kelime örtüşmesine dayanır; embedding tabanlı vektör arama, pgvector indeksleri, JWT/rol bazlı yetkilendirme, tenant izolasyonu, dosya yükleme ve kapsamlı otomatik testler sonraki geliştirme adımlarıdır. Fine-tuning ve 4-bit/8-bit quantization, model eğitim/servisleme süreçleri için dokümante edilen genişletme başlıklarıdır; mevcut compose akışı bunları otomatik uygulamaz.

Geliştirme ortamındaki PostgreSQL parolası örnek amaçlıdır. Canlı ortamda secret yönetimi kullanılmalıdır.

## Anahtar kelimeler

ASP.NET Core, .NET 8, C#, Web API, EF Core, N-Tier Architecture, Clean Architecture, Python, FastAPI, AI Engineering, Artificial Intelligence, Machine Learning, NLP, LLM, Large Language Models, RAG, Retrieval-Augmented Generation, Prompt Engineering, Embeddings, Chunking, Vector Search, Semantic Search, Fine-Tuning, Quantization, 4-bit Quantization, 8-bit Quantization, Ollama, vLLM, OpenAI API, PostgreSQL, pgvector, Redis, Docker, Docker Compose, Nginx, Uvicorn, REST API, Swagger, OpenAPI, CI/CD, GitHub Actions, On-Premise AI, Local LLM, Enterprise AI, Intelligent Support, Ticket Management, Türkçe doğal dil işleme.
