from services.chains.chain_manager import ChainManager

from models.chat_requests import ChatRequest

class BedrockService:
    chain_manager: ChainManager

    def __init__(self):
        self.chain_manager = ChainManager()
    
    def chat_stream(self, chat_requests: ChatRequest):
        chain = self.chain_manager.get_chain(chat_requests.conversation_type)
        chunks = (chain.with_config(
                        configurable={
                            "llm": chat_requests.llm,
                            "prompt": chat_requests.conversation_type,
                            "session_id": chat_requests.session_id,
                        }
                    ).stream(chat_requests.message))
        for chunk in chunks:
            print(chunk)
            if 'answer' in chunk:
                yield chunk['answer']
            else:
                pass
    
    def chat_retrieval(self, chat_requests: ChatRequest):
        chain = self.chain_manager.get_chain(chat_requests.conversation_type)
        chunks = (chain.with_config(
                        configurable={
                            "llm": chat_requests.llm,
                            "prompt": chat_requests.conversation_type,
                            "retrieval": "sample_01",
                            "session_id": chat_requests.session_id,
                        }
                    ).stream(chat_requests.message))
        for chunk in chunks:
            print(chunk)
            if 'answer' in chunk:
                yield chunk['answer']
            else:
                pass