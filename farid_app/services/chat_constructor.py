import logging
from typing import Dict



logger = logging.getLogger(__name__)

class ChatHistoryConstructor:

    @staticmethod
    def construct_chat(conversation_history: dict, n: int = 2, agent_name="AI") -> str:
        try:
            chat_history = ""
            for chat in conversation_history.get("chat", [])[-n:]:
                if chat["by"] == "Assistant" and chat["intent"].get("type") in ["remember", "reminder", "summarize"]:
                    chat_history += f"User: {chat['intent']['query']}\n"

                    if chat["intent"].get("inferred-queries"):
                        chat_history += f'{agent_name}: {{"queries": {chat["intent"].get("inferred-queries")}}}\n'

                    chat_history += f"{agent_name}: {chat['message']}\n\n"
                elif chat["by"] == "Assistant" and chat.get("images"):
                    chat_history += f"User: {chat['intent']['query']}\n"
                    chat_history += f"{agent_name}: [generated image redacted for space]\n"
                elif chat["by"] == "Assistant" and ("excalidraw" in chat["intent"].get("type")):
                    chat_history += f"User: {chat['intent']['query']}\n"
                    chat_history += f"{agent_name}: {chat['intent']['inferred-queries'][0]}\n"
                elif chat["by"] == "User":
                    raw_query_files = chat.get("queryFiles")
                    if raw_query_files:
                        query_files: Dict[str, str] = {}
                        for file in raw_query_files:
                            query_files[file["name"]] = file["content"]

                        query_file_context = ChatHistoryConstructor.gather_raw_query_files(query_files)
                        chat_history += f"User: {query_file_context}\n"
            return chat_history
        
        # Handle unexpected errors
        except Exception as e:
            logger.info(f"Error in constructing chat history {e}")
            return ""