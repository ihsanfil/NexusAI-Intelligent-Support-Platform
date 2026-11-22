from fastapi.testclient import TestClient
from main import app, split_into_chunks, rank_chunks


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["servis"] == "NexusAI AI"


def test_chunking_keeps_document_text():
    chunks = split_into_chunks("NexusAI destek platformu " * 100, size=100, overlap=10)
    assert len(chunks) > 1
    assert all(chunks)


def test_retrieval_prefers_matching_text():
    docs = [
        ("VPN Rehberi", "VPN bağlantısı için kurum hesabı gerekir", "1"),
        ("Yazıcı Rehberi", "Toner değişimi ve kağıt sıkışması", "2"),
    ]
    ranked = rank_chunks("VPN bağlantısı nasıl yapılır", docs)
    assert ranked[0][0] == "VPN Rehberi"
