# Mimari Kararlar

## Servis ayrımı
ASP.NET Core API, talep yönetimi ve kurumsal iş kurallarını yürütür. Python FastAPI servisi LLM çağrıları ve RAG akışını üstlenir. İki servis HTTP/JSON üzerinden haberleşir.

## Veri sorumluluğu
PostgreSQL, destek talepleri ve doküman kayıtları için kalıcı veri katmanıdır. Redis, AI servisinin ilk sürümündeki bilgi dokümanı metinlerini tutar. Bu nedenle doküman metadata kaydı ile AI indeks kaydı farklı servislerde tutulmaktadır.

## RAG akışı
1. Doküman başlık ve metin olarak alınır.
2. Metin örtüşen parçalara ayrılır.
3. Soru ve parçalar arasında Türkçe kelime eşleşmesi yapılır.
4. En uygun ilk beş parça prompt bağlamına eklenir.
5. LLM yalnızca verilen bağlamı kullanarak yanıt üretmeye yönlendirilir.
6. Kullanılan doküman başlıkları kaynak olarak döndürülür.

Mevcut retrieval yöntemi embedding tabanlı değildir. pgvector ve embedding modeli eklenmesi sonraki mimari adımdır.

## Canlı ortam öncesi
JWT/OIDC, rol bazlı yetki, tenant izolasyonu, rate limiting, secret yönetimi, audit log, migration tabanlı şema yönetimi, yedekleme ve gözlemlenebilirlik eklenmelidir.
