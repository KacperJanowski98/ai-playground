import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI

# Phoenix/OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from openinference.instrumentation.openai import OpenAIInstrumentor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Phoenix tracing
def setup_tracing():
    """Setup OpenTelemetry tracing to send data to Phoenix"""
    collector_endpoint = os.getenv("COLLECTOR_ENDPOINT", "http://phoenix:6006/v1/traces")
    
    # Create a resource to identify this service
    resource = Resource.create({
        "service.name": "phoenix-ai-backend",
        "service.version": "1.0.0",
    })
    
    # Create tracer provider
    tracer_provider = trace_sdk.TracerProvider(resource=resource)
    
    # Create OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=collector_endpoint,
        headers={},
    )
    
    # Create span processor
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    # Set the global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    # Instrument OpenAI
    OpenAIInstrumentor().instrument()
    
    logger.info(f"Phoenix tracing initialized with endpoint: {collector_endpoint}")

# Setup tracing
setup_tracing()

# Initialize FastAPI app
app = FastAPI(
    title="Phoenix AI Observability Demo",
    description="A simple backend to test Phoenix AI observability features",
    version="1.0.0"
)

# CORS middleware
cors_origins = [
    "http://localhost:3000",
    "http://frontend:3000",
    os.getenv("PROD_CORS_ORIGIN", "http://localhost:3000")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logger.warning("OPENAI_API_KEY not set - OpenAI features will not work")
    openai_client = None
else:
    openai_client = OpenAI(api_key=openai_api_key)
    logger.info("OpenAI client initialized")

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class ChatResponse(BaseModel):
    message: str
    model: str
    tokens_used: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    message: str

# Routes
@app.get("/api/chat/healthcheck", response_model=HealthResponse)
async def healthcheck():
    """Health check endpoint for container health monitoring"""
    return HealthResponse(
        status="healthy",
        message="Phoenix AI Backend is running"
    )

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="ok", 
        message="Phoenix AI Observability Demo Backend"
    )

@app.post("/api/chat/completion", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """
    Generate chat completion using OpenAI API.
    This endpoint will be traced by Phoenix AI for observability.
    """
    if not openai_client:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured"
        )
    
    try:
        # Get tracer for manual instrumentation if needed
        tracer = trace.get_tracer(__name__)
        
        with tracer.start_as_current_span("chat_completion") as span:
            # Add custom attributes to the span
            span.set_attribute("chat.model", request.model)
            span.set_attribute("chat.temperature", request.temperature)
            span.set_attribute("chat.max_tokens", request.max_tokens)
            span.set_attribute("chat.messages_count", len(request.messages))
            
            # Convert messages to OpenAI format
            messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
            
            logger.info(f"Making OpenAI request with model: {request.model}")
            
            # Make OpenAI API call (this will be automatically traced)
            response = openai_client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            # Extract response data
            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None
            
            # Add response attributes to span
            span.set_attribute("chat.response_tokens", tokens_used or 0)
            span.set_attribute("chat.response_length", len(assistant_message))
            
            logger.info(f"OpenAI response received, tokens used: {tokens_used}")
            
            return ChatResponse(
                message=assistant_message,
                model=request.model,
                tokens_used=tokens_used
            )
            
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")

@app.post("/api/chat/simple")
async def simple_chat(message: str):
    """
    Simple chat endpoint that takes a string message and returns a response.
    Good for quick testing of Phoenix observability.
    """
    if not openai_client:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured"
        )
    
    try:
        tracer = trace.get_tracer(__name__)
        
        with tracer.start_as_current_span("simple_chat") as span:
            span.set_attribute("chat.input_message", message)
            span.set_attribute("chat.type", "simple")
            
            logger.info(f"Simple chat request: {message[:50]}...")
            
            # Create a simple conversation
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Keep responses concise and friendly."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None
            
            span.set_attribute("chat.response_tokens", tokens_used or 0)
            
            logger.info(f"Simple chat response generated, tokens: {tokens_used}")
            
            return {
                "response": assistant_message,
                "tokens_used": tokens_used,
                "model": "gpt-3.5-turbo"
            }
            
    except Exception as e:
        logger.error(f"Error in simple chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Simple chat failed: {str(e)}")

@app.get("/api/test/trace")
async def test_trace():
    """
    Test endpoint to generate a trace without using OpenAI API.
    Useful for testing Phoenix observability without API costs.
    """
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span("test_trace") as span:
        span.set_attribute("test.type", "observability")
        span.set_attribute("test.timestamp", str(trace.get_current_span().get_span_context().span_id))
        
        # Simulate some processing
        import time
        time.sleep(0.1)
        
        with tracer.start_as_current_span("nested_operation") as nested_span:
            nested_span.set_attribute("operation.name", "data_processing")
            nested_span.set_attribute("operation.duration", 0.05)
            time.sleep(0.05)
        
        logger.info("Test trace generated successfully")
        
        return {
            "message": "Test trace generated successfully",
            "trace_id": format(trace.get_current_span().get_span_context().trace_id, '032x'),
            "span_id": format(trace.get_current_span().get_span_context().span_id, '016x')
        }

@app.get("/api/status")
async def get_status():
    """Get backend status and configuration"""
    return {
        "status": "running",
        "openai_configured": openai_client is not None,
        "collector_endpoint": os.getenv("COLLECTOR_ENDPOINT", "http://phoenix:6006/v1/traces"),
        "cors_origins": cors_origins,
        "environment": {
            "instrument_llama_index": os.getenv("INSTRUMENT_LLAMA_INDEX", "false"),
            "prod_cors_origin": os.getenv("PROD_CORS_ORIGIN", "http://localhost:3000")
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
