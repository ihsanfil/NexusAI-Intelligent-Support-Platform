using System.ComponentModel.DataAnnotations;

namespace NexusAI.Api.Contracts;

public sealed record UpdateTicketStatusRequest(
    [Required, RegularExpression("^(Açık|İşlemde|Çözüldü|Kapalı)$")] string Status);
