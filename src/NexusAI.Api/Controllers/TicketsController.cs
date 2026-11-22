using Microsoft.AspNetCore.Mvc;
using NexusAI.Api.Services;

namespace NexusAI.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class TicketsController(AiServiceClient aiService) : ControllerBase
{
    // Talep metnini AI servisine iletir ve analiz sonucunu istemciye döndürür.
    [HttpPost("analyze")]
    [ProducesResponseType(typeof(AiAnalysisResult), StatusCodes.Status200OK)]
    public async Task<IActionResult> Analyze([FromBody] AnalyzeTicketRequest request, CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(request.Text))
            return BadRequest(new { mesaj = "Talep metni boş olamaz." });

        try
        {
            var result = await aiService.AnalyzeAsync(request.Text, cancellationToken);
            return Ok(result);
        }
        catch (HttpRequestException)
        {
            return StatusCode(StatusCodes.Status503ServiceUnavailable,
                new { mesaj = "AI servisine şu anda ulaşılamıyor." });
        }
    }
}

public sealed record AnalyzeTicketRequest(string Text);
