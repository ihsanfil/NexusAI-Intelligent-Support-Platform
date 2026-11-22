using System.ComponentModel.DataAnnotations;

namespace NexusAI.Api.Contracts;

public sealed record CreateTicketRequest(
    [Required, StringLength(200, MinimumLength = 3)] string Title,
    [Required, StringLength(12000, MinimumLength = 5)] string Description);
