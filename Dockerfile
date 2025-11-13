# Dockerfile pro PocketBase
FROM alpine:latest

WORKDIR /app

# Stáhnout PocketBase
ADD https://github.com/pocketbase/pocketbase/releases/latest/download/pocketbase-linux-amd64 /app/pocketbase
RUN chmod +x /app/pocketbase

EXPOSE 8090

CMD ["/app/pocketbase", "serve", "--http=0.0.0.0:8090"]
