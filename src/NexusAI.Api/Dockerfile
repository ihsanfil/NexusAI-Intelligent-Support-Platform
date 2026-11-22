FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY src/NexusAI.Domain/NexusAI.Domain.csproj src/NexusAI.Domain/
COPY src/NexusAI.Infrastructure/NexusAI.Infrastructure.csproj src/NexusAI.Infrastructure/
COPY src/NexusAI.Api/NexusAI.Api.csproj src/NexusAI.Api/
RUN dotnet restore src/NexusAI.Api/NexusAI.Api.csproj
COPY src/ src/
RUN dotnet publish src/NexusAI.Api/NexusAI.Api.csproj -c Release --no-restore -o /app/publish
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "NexusAI.Api.dll"]
