from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from services.llms.bedrock_service import BedrockService

from models.chat_requests import ChatRequest

router = APIRouter()
bedrock_service = BedrockService()

@router.post('/chat/basic')
async def bedrock_chat(chat_requests: ChatRequest):
    return bedrock_service.chat_simple(chat_requests)

@router.post('/chat')
async def bedrock_chat_stream(chat_requests: ChatRequest):
    return StreamingResponse(bedrock_service.chat_stream(chat_requests), media_type='text/event-stream')
