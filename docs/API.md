# API Kullanım Notları

Tüm örnekler yerel geliştirme adresi olan http://localhost:8080 üzerinden verilmiştir.

## Sağlık kontrolü
- GET /health

## Destek talepleri
- POST /api/tickets – Talep oluşturur ve AI sınıflandırması dener.
- GET /api/tickets?page=1&pageSize=20 – Sayfalı talep listesi.
- GET /api/tickets/{id} – Talep detayı.
- PATCH /api/tickets/{id}/status – Talep durumunu günceller.

Durum değerleri: Açık, İşlemde, Çözüldü, Kapalı.

## Bilgi bankası
- POST /api/knowledge – Başlık ve metin içeriğini kaydeder.
- GET /api/knowledge – Eklenen dokümanları listeler.

## AI asistanı
- POST /api/assistant/ask – Bilgi bankası içeriğinden kaynaklı yanıt üretir.

## Örnek JSON

Talep:
```json
{ "title": "VPN bağlantı sorunu", "description": "VPN bağlantısı kurulamıyor." }
```

Durum:
```json
{ "status": "İşlemde" }
```

Doküman:
```json
{ "title": "VPN Rehberi", "content": "VPN bağlantısı için kurum hesabınızla oturum açın ve doğrulamayı tamamlayın." }
```

Soru:
```json
{ "question": "VPN bağlantısı nasıl kurulur?" }
```
