# Standard library imports
import logging
from uuid import uuid4

# Third‑party imports
from asgiref.sync import sync_to_async

# Local application imports
from farid_app.models import Conversation
from farid_app.utils.title_creator import acreate_title_from_query


logger = logging.getLogger(__name__)

async def upsert_conversation(
    conversation_id, agent, query, stream, images, raw_query_files, user_info,tracer
):
    """
    Creates or updates a Conversation instance.
    If conversation_id is empty, creates a new conversation.
    If conversation_id exists, either creates or updates conversation_title if needed.
    Returns the (possibly updated) conversation_id.
    """
    try:
        if not conversation_id:
            conversation_id = str(uuid4())
            conversation_title = await acreate_title_from_query(query, agent=agent,tracer=tracer)
            await sync_to_async(Conversation.objects.create)(
                conversation_id=conversation_id,
                tenant_id=tenant_id,
                conversation_history={"chat": []},
                conversation_title=conversation_title,
                stream=stream,
                images=images if images else [],
                files=raw_query_files if raw_query_files else [],
                user_info=user_info,
                agent=agent.name
            )
        else:
            existing_conversation = await sync_to_async(
                lambda: Conversation.objects.filter(conversation_id=conversation_id).first()
            )()
            if not existing_conversation:
                await sync_to_async(Conversation.objects.create)(
                    conversation_id=conversation_id,
                    tenant_id=tenant_id,
                    conversation_history={"chat": []},
                    conversation_title=query,
                    stream=stream,
                    images=images if images else [],
                    files=raw_query_files if raw_query_files else [],
                    user_info=user_info,
                    agent=agent.name
                )
            else:
                if existing_conversation.conversation_title is None or existing_conversation.conversation_title== "":
                    conversation_title = await acreate_title_from_query(query, agent=agent,tracer=tracer)
                    existing_conversation.conversation_title = conversation_title

                if images:
                    if not existing_conversation.images:
                        existing_conversation.images = []
                    existing_image_ids = set(existing_conversation.images)
                    new_images = [
                        img for img in images if img not in existing_image_ids
                    ]
                    existing_conversation.images.extend(new_images)

                if raw_query_files:
                    if not existing_conversation.files:
                        existing_conversation.files = []
                    existing_file_ids = set(existing_conversation.files)
                    new_files = [
                        file for file in raw_query_files if file not in existing_file_ids
                    ]
                    existing_conversation.files.extend(new_files)

                await sync_to_async(existing_conversation.save)()
                
        tracer["cid"] = conversation_id
        return conversation_id
    except Exception as e:
        logger.error(f"Error in process_conversation for conversation {conversation_id}: {e}")
        return conversation_id