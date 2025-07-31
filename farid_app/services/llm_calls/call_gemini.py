
import os
import aiohttp

from farid_app.schema.chat import ChatSchema


gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_url = os.getenv("GEMINI_API_URL")

async def call_gemini(payload: ChatSchema):
        headers = {
            "Authorization": f"Bearer {gemini_api_key}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            async with session.post(
                gemini_url,
                json=payload.dict(),
                headers=headers,
                timeout=60,
            ) as response:
                response.raise_for_status()
                return await response.json()