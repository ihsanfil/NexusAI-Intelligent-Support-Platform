from main import cosine_similarity, split_into_chunks


def test_chunking_preserves_content():
    text = "NexusAI destek platformu " * 100
    chunks = split_into_chunks(text)
    assert len(chunks) > 1
    assert all(chunks)
    assert chunks[0].startswith("NexusAI destek")


def test_cosine_similarity_identical_vectors():
    assert abs(cosine_similarity([1.0, 0.0], [1.0, 0.0]) - 1.0) < 1e-9


def test_cosine_similarity_orthogonal_vectors():
    assert abs(cosine_similarity([1.0, 0.0], [0.0, 1.0])) < 1e-9


def test_cosine_similarity_different_dimensions():
    assert cosine_similarity([1.0], [1.0, 2.0]) == 0.0
