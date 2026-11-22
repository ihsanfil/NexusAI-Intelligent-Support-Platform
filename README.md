# NexusAI – Akıllı Destek ve Talep Yönetim Platformu

NexusAI, kurumsal destek taleplerini tek noktadan yönetmek; talepleri yapay zekâ yardımıyla sınıflandırmak, önceliklendirmek ve kurum içi dokümanlardan kaynaklı yanıt önerileri üretmek amacıyla geliştirilen bir platformdur.

Ana uygulama C# ve ASP.NET Core Web API üzerinde çalışır. LLM, embedding ve RAG işlemleri Python ve FastAPI ile ayrı bir servis olarak ele alınır. Böylece iş kuralları .NET tarafında, model ve doküman işleme süreçleri AI servisinde tutulur.

## Temel özellikler

- Destek talebi oluşturma, görüntüleme ve durum takibi
- LLM ile talep kategorisi ve öncelik önerisi
- Doküman yükleme, metin çıkarma ve parçalara ayırma (chunking)
- Embedding üretimi ve anlamsal arama (semantic search)
- RAG (Retrieval-Augmented Generation) ile kaynaklı yanıt üretimi
- Yerel / kurum içi LLM çalıştırma: Ollama ve vLLM
- 4-bit ve 8-bit quantization için model servisleme seçenekleri
- ASP.NET Core ile FastAPI arasında REST API entegrasyonu
- PostgreSQL ve pgvector ile kalıcı veri ve vektör arama
- Redis ile önbellekleme
- Docker Compose ve Nginx ile dağıtım altyapısı

## Teknoloji yığını

| Alan | Teknolojiler |
|---|---|
| Backend | C#, .NET 8, ASP.NET Core Web API |
| Mimari | N-Tier Architecture, katmanlı mimari, DTO, servis katmanı |
| AI servisi | Python, FastAPI, Pydantic, Uvicorn |
| LLM | Ollama, vLLM, OpenAI uyumlu API |
| RAG | Embeddings, chunking, prompt engineering, semantic search, vector search |
| Veri | PostgreSQL, pgvector, Redis |
| Dağıtım | Docker, Docker Compose, Nginx |
| API dokümantasyonu | Swagger, OpenAPI |
| Test ve otomasyon | xUnit, pytest, CI/CD, GitHub Actions |

## Genel mimari

```text
İstemci
  |
Nginx (Reverse Proxy)
  |
ASP.NET Core Web API
  |                    |
PostgreSQL             Redis
  |
Python FastAPI AI Servisi
  |
Embedding / RAG / LLM
  |
Ollama veya vLLM
```

ASP.NET Core tarafı talep yönetimi, doğrulama, yetkilendirme ve uygulama kurallarını yürütür. Python servisi doküman işleme, embedding, retrieval ve model çağrılarını üstlenir.

## Planlanan depo düzeni

- `src/NexusAI.Api` – HTTP uç noktaları ve API yapılandırması
- `src/NexusAI.Application` – uygulama servisleri ve iş akışları
- `src/NexusAI.Domain` – varlıklar ve iş kuralları
- `src/NexusAI.Infrastructure` – veri erişimi ve dış servis bağlantıları
- `ai-service` – FastAPI tabanlı AI ve RAG servisi
- `deploy` – Docker ve Nginx yapılandırmaları
- `docs` – mimari ve geliştirme dokümanları

## Geliştirme ve çalıştırma

Proje aktif geliştirme aşamasındadır. Henüz tamamlanmamış veya test edilmemiş bileşenler tamamlanmış gibi gösterilmez. Çalıştırma adımları ve gerekli ortam değişkenleri, ilgili servisler eklendikçe bu dosyada güncellenecektir.

## Güvenlik

Gerçek ortamda kimlik doğrulama, rol bazlı yetkilendirme, tenant bazlı veri ayrımı, istek sınırlandırma, gizli anahtar yönetimi ve loglarda hassas veri maskeleme uygulanmalıdır. Depoda gerçek parola veya API anahtarı tutulmamalıdır.

## Anahtar kelimeler

ASP.NET Core, .NET 8, C#, Web API, Python, FastAPI, AI Engineering, Artificial Intelligence, Machine Learning, NLP, LLM, Large Language Models, RAG, Retrieval-Augmented Generation, Prompt Engineering, Embeddings, Vector Database, pgvector, Vector Search, Semantic Search, Chunking, Fine-Tuning, Quantization, 4-bit Quantization, 8-bit Quantization, Ollama, vLLM, OpenAI API, PostgreSQL, Redis, Docker, Docker Compose, Nginx, Uvicorn, REST API, N-Tier Architecture, Clean Architecture, Swagger, OpenAPI, CI/CD, GitHub Actions, On-Premise AI, Local LLM, Production Deployment, Enterprise AI, Intelligent Support, Ticket Management, Türkçe doğal dil işleme.

## Lisans

Lisans koşulları proje yayın öncesinde netleştirilecektir.
