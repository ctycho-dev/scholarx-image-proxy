# ScholarX Image Proxy

Bypass Russian ISP throttling of Cloudflare R2 images (16KB limit since June 2025).

## Quick Start

1. **Deploy:**
```bash
git clone <repo-url>
cd scholarx-image-proxy
cp .env.example .env
docker compose up -d
```

2. **Configure `.env`:**
```bash
R2_BASE_URL=https://scholarx.mypinx.store
```

3. **Test:**
```bash
# Health check
curl http://YOUR_VPS_IP/api/v1/health

# Test image (check X-Cache-Status header)
curl -I http://YOUR_VPS_IP/api/v1/home/main/circle.png
```

## Frontend Integration

```typescript
const PROXY_URL = 'http://YOUR_VPS_IP';
const R2_BASE_URL = 'https://scholarx.mypinx.store';

export const getImageUrl = (path: string): string => {
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    return isRussianUser ? `${PROXY_URL}/api/v1/${cleanPath}` : `${R2_BASE_URL}/${cleanPath}`;
};
```

## Performance

- **Cache MISS:** 200-300ms (first request)
- **Cache HIT:** 1-2ms (99%+ of requests)
- **Capacity:** 10,000+ req/s

## Monitoring

```bash
# View logs
docker compose logs -f

# Check status
docker compose ps
```

## Troubleshooting

**Images not loading:**
```bash
docker compose logs fastapi
```

**Nginx errors:**
```bash
docker compose logs nginx
docker exec scholarx-nginx nginx -t
```

## SSL Setup (Production)

```bash
sudo certbot certonly --standalone -d proxy.scholarx.com
```

Update `nginx/nginx.conf` with your domain and uncomment SSL section.

## Requirements

- Docker & Docker Compose
- 2GB+ RAM
- 10GB disk space
