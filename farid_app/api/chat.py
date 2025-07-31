
from ninja_extra import api_controller, http_post
from django.http import JsonResponse
import logging
import os

from farid_app.schema.chat import ChatSchema
from farid_app.models import Conversation
from farid_app.services.chat_constructor import ChatHistoryConstructor
from farid_app.services.llm_calls.call_khoj import call_khoj
from farid_app.services.llm_calls.call_gemini import call_gemini


logger = logging.getLogger(__name__)

khoj_api_key = os.getenv("OPENAI_API_KEY2")
khoj_url = os.getenv("KHOJ_API_BASE_URL")

@api_controller("v1/agent", tags=["Agent"])
class AgentController:
    @http_post("/chat", response=None, description="Chat with the agent")
    async def chat(self, request, payload: ChatSchema):
        response_data = None
        errors = []
        for name, func in [
            ("Khoj", call_khoj),
            ("Gemini", call_gemini),
        ]:
            try:
                response_data = await func(payload)
                logger.info(f"{name} succeeded.")
                break  # success, stop the fallback chain
            except Exception as e:
                logger.warning(f"{name} failed: {e}")
                errors.append(f"{name}: {str(e)}")

        if response_data is None:
            logger.error("All AI services failed.")
            return JsonResponse({
                "error": "All AI services failed",
                "details": errors
            }, status=502)
        

        # Optionally log conversation
        try:
            Conversation.conversation_log = ChatHistoryConstructor.construct_chat(payload)
        except Exception as log_error:
            logger.warning(f"Conversation log failed: {log_error}")

        return JsonResponse(response_data, status=200)