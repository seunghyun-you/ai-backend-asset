from services.apis import bedrock_api_manager
from services.templates import chat_template
from services.retrievals.retrieval_manager import retrievalManager
from services.memory.in_memory_history import InMemoryHistory

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableField, RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.globals import set_debug
set_debug(True)
store = {}

retrieval_manager = retrievalManager()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory(max_messages=5)
    return store[session_id]

def memory_chain(chain):
    message_history_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    return RunnableParallel(
        {
            "input": RunnablePassthrough()
        }
    ).assign(answer=message_history_chain)

def retrieval_chain(chain):
    retrieval = retrieval_manager.get_configurable_retrievals()
    message_history_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    return RunnableParallel(
        {
            "input": RunnablePassthrough(),
            "source_documents": retrieval
        }
    ).assign(answer=message_history_chain)

chain_dictionary = {
    "general": memory_chain,
    "retrieval": retrieval_chain,
}

def create_chain(chain_type: str = 'general'):
    llm = bedrock_api_manager.get_configurable_llm()
    prompt = chat_template.get_configurable_template()
    _chain = prompt | llm | StrOutputParser()

    chain = chain_dictionary.get(chain_type)
    return chain(_chain)

class ChainManager:
    chains = {}
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.chains['general'] = create_chain(chain_type='general')
        self.chains['retrieval'] = create_chain(chain_type='retrieval')
    
    def get_chain(self, conversation_type: str = 'getneral'):
        return self.chains[conversation_type]