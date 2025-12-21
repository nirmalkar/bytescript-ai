import time
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel

from app.core.auth import require_user
from app.core.rate_limit import enforce_usage
from app.db.connection import get_db
from app.db.crud_operations import increment_usage
from app.llm.deepseek import generate_reply
from app.llm.prompt import build_prompt

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: Optional[int] = None

@router.post("/chat/completions")
async def chat_completion(
    request: ChatRequest,
    user=Depends(require_user),
    db=Depends(get_db)
):
    # Enforce usage limits
    enforce_usage(user, db)
    
    # Increment usage for this request
    increment_usage(db, user["uid"])
    
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="No messages provided")
            
        # Get the last user message
        last_message = request.messages[-1]
        if last_message.role != "user":
            raise HTTPException(
                status_code=400, 
                detail="Last message must be from user"
            )
        
        # Build and send the prompt to DeepSeek
        prompt = build_prompt(last_message.content)
        start_time = time.time()
        response_text = await generate_reply(
            prompt=prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        processing_time = time.time() - start_time
        
        # Estimate token usage (approximate)
        prompt_tokens = len(prompt.split())
        completion_tokens = len(response_text.split())
        
        return {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
                "processing_time_seconds": round(processing_time, 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
