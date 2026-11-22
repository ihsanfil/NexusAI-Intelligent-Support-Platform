using System.Net.Http.Json;

namespace NexusAI.Api.Services;

public sealed class AiServiceClient(HttpClient httpClient)
{
    // Talep metnini AI servisine gönderir, sınıflandırma ve yanıt önerisini alır.
    public async Task<AiAnalysisResult?> AnalyzeAsync(string text, CancellationToken cancellationToken)
    {
        using var response = await httpClient.PostAsJsonAsync("/analyze", new { text }, cancellationToken);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<AiAnalysisResult>(cancellationToken: cancellationToken);
    }

    // Bilgi bankasındaki içeriklere dayanarak RAG yanıtı üretir.
    public async Task<RagAnswerResult?> AskAsync(string question, CancellationToken cancellationToken)
    {
        using var response = await httpClient.PostAsJsonAsync("/ask", new { question }, cancellationToken);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<RagAnswerResult>(cancellationToken: cancellationToken);
    }
}
public sealed record AiAnalysisResult(string category, string priority, string answer, IReadOnlyList<string> sources);
public sealed record RagAnswerResult(string answer, IReadOnlyList<string> sources);