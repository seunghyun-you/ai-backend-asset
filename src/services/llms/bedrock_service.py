from langchain_community.chat_message_histories import SQLChatMessageHistory

from models.chat_requests import ChatRequest
from services.chains.chain_manager import ChainManager
from services.repositories.chat_history_repositories import ChatHistoryRepository

class BedrockService:
    chain_manager: ChainManager

    def __init__(self):
        self.chain_manager = ChainManager()
        self.chat_history_repository = ChatHistoryRepository()
    
    def chat_simple(self, message:str = None):
        chain = self.chain_manager.get_chain('simple')
        response = (chain.with_config(
                        configurable={
                            "llm": 'haiku',
                            "prompt": 'simple',
                        }).invoke(message))
        return response['answer']

    def chat_stream(self, chat_requests: ChatRequest):
        ai_message = ""
        chain = self.chain_manager.get_chain(chat_requests.conversation_type)
        response = (chain.with_config(
                        configurable={
                            "llm": chat_requests.llm,
                            "prompt": chat_requests.conversation_type,
                            "session_id": chat_requests.session_id,
                        }
                    ).stream(chat_requests.message))
        
        for chunk in response:
            if 'answer' in chunk:
                ai_message = ai_message + chunk['answer']
                yield chunk['answer']
            else:
                pass

        result = self.chat_history_repository.check_chat_room_exists(chat_requests)
        if result:
            self.chat_history_repository.save_user_message(chat_requests)
            self.chat_history_repository.update_total_chat_count(chat_requests)
        else:
            chat_room_title= self.chat_simple(chat_requests.message)
            self.chat_history_repository.add_chat_room_list(chat_requests, chat_room_title)
            self.chat_history_repository.save_user_message(chat_requests)

        self.chat_history_repository.save_ai_message(chat_requests, ai_message)
    
    def chat_retrieval(self, chat_requests: ChatRequest):
        chain = self.chain_manager.get_chain(chat_requests.conversation_type)
        response = (chain.with_config(
                        configurable={
                            "llm": chat_requests.llm,
                            "prompt": chat_requests.conversation_type,
                            "retrieval": "sample_01",
                            "session_id": chat_requests.session_id,
                        }
                    ).stream(chat_requests.message))
        for chunk in response:
            if 'answer' in chunk:
                yield chunk['answer']
            else:
                pass