using Microsoft.EntityFrameworkCore;
using NexusAI.Api.Services;
using NexusAI.Infrastructure.Data;
using StackExchange.Redis;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddDbContext<NexusAiDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddSingleton<IConnectionMultiplexer>(_ =>
    ConnectionMultiplexer.Connect((builder.Configuration.GetConnectionString("Redis") ?? "localhost:6379") + ",abortConnect=false"));
builder.Services.AddHttpClient<AiServiceClient>(client =>
{
    client.BaseAddress = new Uri(builder.Configuration["AiService:BaseUrl"] ?? "http://localhost:8000");
    client.Timeout = TimeSpan.FromSeconds(120);
});

var app = builder.Build();
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
app.MapControllers();
app.MapGet("/health", async (NexusAiDbContext db, IConnectionMultiplexer redis) =>
{
    var databaseOk = await db.Database.CanConnectAsync();
    var redisOk = await redis.GetDatabase().PingAsync() > TimeSpan.Zero;
    return Results.Ok(new { durum = databaseOk && redisOk ? "sağlıklı" : "kısmi", postgres = databaseOk, redis = redisOk });
});
app.Run();
