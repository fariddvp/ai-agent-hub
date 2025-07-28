from ninja_extra import api_controller, http_post, ControllerBase
from django.http import JsonResponse
import aiohttp
from aiohttp import ClientTimeout
from aiohttp.client_exceptions import ClientError, ClientResponseError
import logging
import os
from asyncio import TimeoutError as AsyncTimeoutError

from farid_app.schema.chat import ChatSchema



logger = logging.getLogger(__name__)

khoj_api_key = os.getenv("OPENAI_API_KEY2")
khoj_url = os.getenv("KHOJ_API_BASE_URL")

@api_controller("v1/agent", tags=["Agent"])
class AgentController:
    @http_post("/chat", response=None, description="Chat with the agent")
    async def chat(self, request, payload: ChatSchema):
        try:

            headers = {
                "Authorization": f"Bearer {khoj_api_key}",
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(
                    khoj_url,
                    json=payload.dict(),
                    headers=headers,
                    timeout=60,
                ) as response:
                    logger.info(f"Khoj API response status: {response.status}")
                    response.raise_for_status()
                    data = await response.json()
        except AsyncTimeoutError:
            return JsonResponse({"error": "Khoj API request timed out"}, status=504)
        except aiohttp.ClientResponseError as e:
            logger.error(f"KHOJ API error: {e.status} - {e.message}")
            return JsonResponse({"error": f"Khoj API error: {e.status}"}, status=e.status)
        except Exception as e:
            logger.exception(f"Unexpected error occurred: {str(e)}")
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

        return JsonResponse(data, status=200)