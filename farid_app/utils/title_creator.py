


import logging

from taavagent.services.generalservices.general_services import send_message_to_model_wrapper
from taavagent.prompts import prompts
from taavagent.utils.utils import timer

logger = logging.getLogger(__name__)


async def acreate_title_from_query(query: str = "",agent=None, tracer:dict={}) -> str:
    """
    Create a title from the given query
    """
    logger.info(f"Creating title from query: {agent.name}")
    chat_model = agent.chat_model
    model_type = agent.model_type
    max_tokens = agent.max_prompt_size
    
    title_generation_prompt = prompts.subject_generation.format(query=query)
    try:
        with timer("Chat actor: Generate title from query", logger):
            response, tracer = await send_message_to_model_wrapper(
                query=query,
                system_message=title_generation_prompt,
                chat_model=chat_model,
                model_type=model_type,
                max_token=max_tokens,
                tracer=tracer
            )
    except : 
        response = "Starting a New Chat"

    logger.info(f"Title generated: {response}")
    if response is None or response.strip() == "":
        response = "Starting a New Chat"

    return response