using Microsoft.EntityFrameworkCore;
using NexusAI.Domain.Entities;

namespace NexusAI.Infrastructure.Data;

public sealed class NexusAiDbContext(DbContextOptions<NexusAiDbContext> options) : DbContext(options)
{
    public DbSet<Ticket> Tickets => Set<Ticket>();
    public DbSet<KnowledgeDocument> KnowledgeDocuments => Set<KnowledgeDocument>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Ticket>(entity =>
        {
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Title).HasMaxLength(200).IsRequired();
            entity.Property(x => x.Description).HasMaxLength(12000).IsRequired();
            entity.Property(x => x.Status).HasMaxLength(40);
            entity.Property(x => x.Priority).HasMaxLength(40);
            entity.HasIndex(x => x.CreatedAtUtc);
        });
        modelBuilder.Entity<KnowledgeDocument>(entity =>
        {
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Title).HasMaxLength(300).IsRequired();
            entity.Property(x => x.Content).IsRequired();
        });
    }
}