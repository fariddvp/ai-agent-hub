
import os
import aiohttp

from farid_app.schema.chat import ChatSchema

khoj_api_key = os.getenv("OPENAI_API_KEY2")
khoj_url = os.getenv("KHOJ_API_BASE_URL")

async def call_khoj(payload: ChatSchema):
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
                response.raise_for_status()
                return await response.json()