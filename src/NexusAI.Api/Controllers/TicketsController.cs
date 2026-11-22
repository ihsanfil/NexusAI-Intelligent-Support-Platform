using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using NexusAI.Api.Contracts;
using NexusAI.Api.Services;
using NexusAI.Domain.Entities;
using NexusAI.Infrastructure.Data;

namespace NexusAI.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class TicketsController(NexusAiDbContext db, AiServiceClient aiService) : ControllerBase
{
    // Yeni talebi kaydeder; AI servisi erişilebilirse sınıflandırma önerisini de ekler.
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateTicketRequest request, CancellationToken cancellationToken)
    {
        var ticket = new Ticket { Title = request.Title.Trim(), Description = request.Description.Trim() };
        try
        {
            var analysis = await aiService.AnalyzeAsync(ticket.Description, cancellationToken);
            if (analysis is not null)
            {
                ticket.Category = analysis.category;
                ticket.Priority = analysis.priority;
                ticket.AiSuggestion = analysis.answer;
            }
        }
        catch (HttpRequestException)
        {
            // AI servisi geçici olarak kapalı olsa da talebi kaybetmeden kaydediyoruz.
        }
        db.Tickets.Add(ticket);
        await db.SaveChangesAsync(cancellationToken);
        return CreatedAtAction(nameof(GetById), new { id = ticket.Id }, ticket);
    }

    [HttpGet]
    public async Task<IActionResult> List([FromQuery] int page = 1, [FromQuery] int pageSize = 20, CancellationToken cancellationToken = default)
    {
        page = Math.Max(1, page);
        pageSize = Math.Clamp(pageSize, 1, 100);
        var query = db.Tickets.AsNoTracking().OrderByDescending(x => x.CreatedAtUtc);
        var total = await query.CountAsync(cancellationToken);
        var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync(cancellationToken);
        return Ok(new { page, pageSize, total, items });
    }

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetById(Guid id, CancellationToken cancellationToken)
    {
        var ticket = await db.Tickets.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id, cancellationToken);
        return ticket is null ? NotFound() : Ok(ticket);
    }

    [HttpPatch("{id:guid}/status")]
    public async Task<IActionResult> UpdateStatus(Guid id, [FromBody] UpdateTicketStatusRequest request, CancellationToken cancellationToken)
    {
        var ticket = await db.Tickets.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);
        if (ticket is null) return NotFound();
        ticket.Status = request.Status;
        ticket.UpdatedAtUtc = DateTime.UtcNow;
        await db.SaveChangesAsync(cancellationToken);
        return Ok(ticket);
    }
}