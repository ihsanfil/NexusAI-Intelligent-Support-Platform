using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexusAI.Api.Contracts;
using NexusAI.Infrastructure.Data;

namespace NexusAI.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class KnowledgeController(NexusAiDbContext db, IHttpClientFactory clients, IConfiguration configuration) : ControllerBase
{
    // Dokümanı önce veritabanına kaydeder, ardından RAG servisinin arama havuzuna ekler.
    [HttpPost]
    public async Task<IActionResult> Add([FromBody] AddKnowledgeRequest request, CancellationToken cancellationToken)
    {
        var document = new NexusAI.Domain.Entities.KnowledgeDocument { Title = request.Title, Content = request.Content };
        db.KnowledgeDocuments.Add(document);
        await db.SaveChangesAsync(cancellationToken);

        var baseUrl = configuration["AiService:BaseUrl"] ?? "http://localhost:8000";
        var client = clients.CreateClient();
        try
        {
            var response = await client.PostAsJsonAsync($"{baseUrl}/knowledge", new { title = request.Title, content = request.Content }, cancellationToken);
            response.EnsureSuccessStatusCode();
        }
        catch (HttpRequestException)
        {
            // Kayıt veritabanında durur; AI servisi açıldığında tekrar indekslenebilir.
            return StatusCode(202, new { document.Id, mesaj = "Doküman kaydedildi ancak AI indekslemesi tamamlanamadı." });
        }
        return Created($"/api/knowledge/{document.Id}", new { document.Id, document.Title });
    }

    [HttpGet]
    public async Task<IActionResult> List(CancellationToken cancellationToken)
    {
        var documents = await db.KnowledgeDocuments.AsNoTracking()
            .OrderByDescending(x => x.CreatedAtUtc)
            .Select(x => new { x.Id, x.Title, x.CreatedAtUtc }).ToListAsync(cancellationToken);
        return Ok(documents);
    }
}

public sealed record AddKnowledgeRequest(
    [System.ComponentModel.DataAnnotations.Required, System.ComponentModel.DataAnnotations.StringLength(300)] string Title,
    [System.ComponentModel.DataAnnotations.Required, System.ComponentModel.DataAnnotations.StringLength(50000, MinimumLength = 20)] string Content);
