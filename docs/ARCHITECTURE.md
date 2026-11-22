# Mimari ve teknik kararlar

## Servis sınırları

- **NexusAI.Api:** ASP.NET Core 8 REST API. Talep kayıtlarını ve doküman metadata bilgilerini PostgreSQL'de tutar.
- **NexusAI.Domain:** İş varlıkları.
- **NexusAI.Infrastructure:** EF Core veri erişimi.
- **ai-service:** FastAPI üzerinden sınıflandırma, embedding ve RAG iş akışlarını yürütür.
- **web:** React tabanlı yönetim ekranı, Nginx ile statik yayın ve API reverse proxy.
- **Ollama:** Yerel LLM ve embedding modellerini sunar.
- **Redis:** Doküman parçalarını ve embedding vektörlerini saklar.

## RAG akışı

1. Doküman API'ye gönderilir ve PostgreSQL metadata kaydı oluşturulur.
2. AI servisi metni yaklaşık 900 karakterlik, 120 karakter örtüşmeli parçalara ayırır.
3. Her parça `nomic-embed-text` ile vektöre dönüştürülür ve Redis'e yazılır.
4. Soru geldiğinde aynı embedding modeliyle soru vektörü çıkarılır.
5. Cosine similarity ile en yakın beş parça seçilir.
6. Seçilen parçalar kaynak başlıklarıyla LLM'e bağlam olarak verilir.

Bu ilk uygulama küçük/orta hacimli demo içindir. Redis anahtarlarının toplu taranması büyük veri için uygun değildir. Üretimde pgvector/Redis Vector Search, indeksleme kuyruğu, yeniden indeksleme ve silme senaryoları eklenmelidir.

## Model seçimi ve quantization

Varsayılan üretim modeli `llama3.2:3b`, embedding modeli `nomic-embed-text` olarak ayarlanmıştır. Ollama model paketleri kendi quantization biçimleriyle sunulabilir. 4-bit/8-bit quantization ve vLLM, donanım ve model uyumluluğuna göre alternatif dağıtım seçenekleridir; mevcut Compose akışı otomatik fine-tuning yapmaz.

## Canlıya geçiş kontrol listesi

- JWT/OIDC kimlik doğrulama ve rol bazlı yetkilendirme
- Secret manager ile parola ve anahtar yönetimi
- Rate limiting, audit log ve hassas veri maskeleme
- Dosya yükleme için MIME doğrulama, boyut sınırı ve zararlı içerik taraması
- Tenant bazlı veri izolasyonu
- EF Core migration ve kontrollü deployment
- Redis ACL/TLS, PostgreSQL ağ kısıtları ve yedekleme
- RAG prompt injection kontrolleri ve kaynak erişim yetkisi
- Telemetri, tracing, metrikler ve alarm yönetimi
