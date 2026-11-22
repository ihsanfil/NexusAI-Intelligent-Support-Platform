using System.Net.Http.Json;

namespace NexusAI.Api.Services;

public sealed class AiServiceClient(HttpClient httpClient)
{
    // AI servisine gelen metni gönderir, sınıflandırma ve yanıt önerisini alır.
    public async Task<AiAnalysisResult?> AnalyzeAsync(string text, CancellationToken cancellationToken)
    {
        using var response = await httpClient.PostAsJsonAsync("/analyze", new { text }, cancellationToken);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<AiAnalysisResult>(cancellationToken: cancellationToken);
    }
}

public sealed record AiAnalysisResult(string category, string priority, string answer, IReadOnlyList<string> sources);
