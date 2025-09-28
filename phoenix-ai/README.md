# 🔥 Phoenix AI Observability Demo

This project demonstrates how to integrate [Phoenix AI](https://phoenix.arize.com/) observability tool with a simple AI application to monitor, trace, and debug LLM interactions.

## 🎯 What This Demo Includes

- **Phoenix AI Observability Platform**: Self-hosted observability dashboard for LLM applications
- **FastAPI Backend**: Python backend with OpenAI integration and automatic tracing
- **Simple Frontend**: Web interface to interact with the backend and generate traces
- **OpenTelemetry Integration**: Automatic instrumentation of OpenAI API calls
- **Docker Compose Setup**: Everything runs in containers for easy setup

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Frontend      │────│   Backend       │────│   Phoenix AI    │
│   (Port 3000)   │    │   (Port 8000)   │    │   (Port 6006)   │
│                 │    │                 │    │                 │
│ - Web Interface │    │ - FastAPI       │    │ - Observability │
│ - Test Controls │    │ - OpenAI Client │    │ - Trace Viewer  │
│ - Status Check  │    │ - Auto Tracing  │    │ - Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │                 │
                    │   OpenAI API    │
                    │                 │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API Key (optional, but recommended for full functionality)

### 1. Set Up Environment

```bash
# Navigate to the phoenix-ai directory
cd phoenix-ai

# Copy the environment template
cp .env.template .env

# Edit .env and add your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 2. Start the Application

```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 3. Access the Applications

Once the containers are running, you can access:

- **Frontend**: http://localhost:3000 - Interactive demo interface
- **Phoenix Dashboard**: http://localhost:6006 - Observability dashboard
- **Backend API**: http://localhost:8000/docs - FastAPI documentation
- **Backend Status**: http://localhost:8000/api/status - Configuration check

## 🔍 What You'll See in Phoenix

### Phoenix Dashboard Features

1. **Traces Timeline**: View all LLM interactions chronologically
2. **Span Details**: Drill down into individual API calls
3. **Performance Metrics**: Monitor latency, token usage, and errors
4. **Request/Response Data**: See exact prompts and completions
5. **Error Tracking**: Identify and debug failed requests

### Automatically Traced Data

- **OpenAI API Calls**: Every completion request is traced
- **Request Parameters**: Model, temperature, max_tokens, etc.
- **Response Metadata**: Token usage, completion time, model version
- **Custom Attributes**: User messages, response length, trace IDs
- **Error Information**: Stack traces and error details

## 🧪 Testing the Observability

### 1. Simple Chat Test
- Send a message to OpenAI and see the trace in Phoenix
- View request/response data and performance metrics

### 2. Advanced Chat Completion
- Test different models (GPT-3.5, GPT-4)
- Adjust parameters (temperature, max_tokens)
- Compare performance across different configurations

### 3. Test Trace (No API Cost)
- Generate traces without calling OpenAI
- Verify Phoenix observability is working
- Test trace structure and attributes

### 4. Backend Status Check
- Verify configuration and connectivity
- Check OpenAI API key setup
- Monitor backend health

## 📊 Key Phoenix Features to Explore

### Trace Analysis
- Click on any trace in the Phoenix dashboard
- Explore the span hierarchy and timing
- View all attributes and metadata

### Performance Monitoring
- Monitor response times and token usage
- Identify slow or expensive requests
- Track usage patterns over time

### Debugging
- View exact prompts and responses
- Identify failed requests and error patterns
- Debug model parameter effects

### Data Export
- Export traces for further analysis
- Create custom dashboards and reports
- Integrate with other monitoring tools

## 🛠️ Customization

### Adding Custom Traces
You can add custom traces to any part of your application:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Your code here
```

### Environment Variables
Configure the application through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `COLLECTOR_ENDPOINT`: Phoenix trace collector endpoint
- `INSTRUMENT_LLAMA_INDEX`: Enable/disable LlamaIndex instrumentation
- `PROD_CORS_ORIGIN`: CORS origin for production

### Adding More LLM Providers
Phoenix supports many LLM providers through OpenInference:

- AWS Bedrock
- Anthropic Claude
- Google Vertex AI
- LiteLLM
- Local models

## 🔧 Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Phoenix Development
```bash
# Run Phoenix locally without Docker
pip install arize-phoenix
python -m phoenix.server.main serve
```

## 📚 Learn More

### Phoenix AI Documentation
- [Official Documentation](https://docs.arize.com/phoenix)
- [GitHub Repository](https://github.com/Arize-ai/phoenix)
- [OpenInference Specification](https://github.com/Arize-ai/openinference)

### OpenTelemetry
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Auto-Instrumentation](https://opentelemetry.io/docs/languages/python/automatic/)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI/Swagger](http://localhost:8000/docs)

## 🐛 Troubleshooting

### Common Issues

1. **Phoenix Dashboard Not Loading**
   - Check if Phoenix container is running: `docker-compose ps`
   - Verify port 6006 is not in use
   - Check logs: `docker-compose logs phoenix`

2. **Backend API Errors**
   - Verify OpenAI API key is set correctly
   - Check backend logs: `docker-compose logs backend`
   - Ensure ports 8000 is available

3. **No Traces Appearing**
   - Verify `COLLECTOR_ENDPOINT` environment variable
   - Check OpenTelemetry instrumentation setup
   - Ensure Phoenix is receiving traces on port 4317 (gRPC) or 6006 (HTTP)

4. **Frontend Connection Issues**
   - Check if backend is healthy: http://localhost:8000/api/status
   - Verify CORS configuration
   - Check browser developer tools for errors

### Logs and Debugging
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs phoenix
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

## 🎮 Next Steps

After exploring this demo, you can:

1. **Integrate with Your Application**: Add Phoenix observability to your existing LLM applications
2. **Explore Advanced Features**: Set up evaluations, experiments, and prompt management
3. **Scale to Production**: Deploy Phoenix with PostgreSQL backend for production use
4. **Add More Providers**: Instrument other LLM providers and frameworks
5. **Custom Analytics**: Build custom dashboards and analysis workflows

## 🤝 Contributing

Feel free to contribute improvements to this demo:

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 📝 License

This demo is provided as-is for educational and demonstration purposes.
