# EV Car Telegram Bot - Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Valid Telegram Bot Token
- Access to the API endpoints

## Environment Setup

1. **Environment Variables**
   Create a `.env` file with the following variables:
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   API_BASE_URL=https://inventoryapiv1-367404119922.asia-southeast1.run.app
   API_BASE_URL_IMG=https://pub-133f8593b35749f28fa090bc33925b31.r2.dev
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   API_TIMEOUT=30
   ```

## Deployment Options

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd ev_car_telegrambot

# Create and configure .env file
cp .env.example .env
# Edit .env with your actual values

# Build and start the bot
docker-compose up -d

# Check logs
docker-compose logs -f telegram-bot

# Stop the bot
docker-compose down
```

### Option 2: Docker Only

```bash
# Build the image
docker build -t ev-car-telegram-bot .

# Run the container
docker run -d \
  --name ev-car-bot \
  --env-file .env \
  --restart unless-stopped \
  ev-car-telegram-bot
```

### Option 3: Direct Python

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_chat_id
# ... other variables

# Run the bot
python main.py
```

## Cloud Deployment

### Heroku
1. Create a `Procfile`:
   ```
   worker: python main.py
   ```
2. Set environment variables in Heroku dashboard
3. Deploy using Git or GitHub integration

### Google Cloud Run
1. Build and push to Google Container Registry
2. Deploy to Cloud Run with environment variables
3. Set minimum instances to 1 for always-on bot

### AWS ECS/Fargate
1. Push image to ECR
2. Create ECS task definition with environment variables
3. Deploy as ECS service

## Monitoring

- Check bot health: `docker-compose logs telegram-bot`
- Monitor API calls and response times
- Set up alerts for bot downtime

## Security Considerations

- Never commit `.env` file to version control
- Use secrets management in production
- Regularly update dependencies
- Monitor for security vulnerabilities

## Troubleshooting

1. **Bot not responding**: Check TELEGRAM_TOKEN validity
2. **API errors**: Verify API_BASE_URL accessibility
3. **Memory issues**: Monitor container resource usage
4. **Network issues**: Check firewall and network policies

## Scaling

- For high traffic, consider using webhooks instead of polling
- Implement rate limiting and request queuing
- Use load balancers for multiple bot instances