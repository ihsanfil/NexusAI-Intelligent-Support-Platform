using Microsoft.AspNetCore.Mvc;
using NexusAI.Api.Services;

namespace NexusAI.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class AssistantController(AiServiceClient aiService) : ControllerBase
{
    // Kullanıcının sorusunu bilgi bankası üzerinden yanıtlatır.
    [HttpPost("ask")]
    public async Task<IActionResult> Ask([FromBody] AskRequest request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Question))
            return BadRequest(new { mesaj = "Soru boş olamaz." });
        try
        {
            var result = await aiService.AskAsync(request.Question, cancellationToken);
            return Ok(result);
        }
        catch (HttpRequestException)
        {
            return StatusCode(503, new { mesaj = "AI servisine şu anda ulaşılamıyor." });
        }
    }
}
public sealed record AskRequest(string Question);
