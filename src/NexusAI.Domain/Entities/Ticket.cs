namespace NexusAI.Domain.Entities;

public sealed class Ticket
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    public string Category { get; set; } = "Genel";
    public string Priority { get; set; } = "Orta";
    public string Status { get; set; } = "Açık";
    public string? AiSuggestion { get; set; }
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAtUtc { get; set; } = DateTime.UtcNow;
}