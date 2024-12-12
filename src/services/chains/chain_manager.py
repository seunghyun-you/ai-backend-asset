from services.apis import bedrock_api_manager
from services.templates import chat_template
from services.retrievers.retriever_manager import RetrieverManager
from services.memory.in_memory_history import InMemoryHistory

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableField, RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.globals import set_debug
set_debug(True)
store = {}

retriever_manager = RetrieverManager()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory(max_messages=5)
    return store[session_id]

def basic_chain(chain):
    return RunnableParallel(
        {
            "input": RunnablePassthrough()
        }
    ).assign(answer=chain)

def memory_chain(chain):
    runnable_with_message_history_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    return RunnableParallel(
        {
            "input": RunnablePassthrough()
        }
    ).assign(answer=runnable_with_message_history_chain)

def retriever_chain(chain):
    retriever = retriever_manager.get_configurable_retrievers()

    return RunnableParallel(
        {
            "input": RunnablePassthrough(),
            "source_documents": retriever
        }
    ).assign(answer=chain)

chain_dictionary = {
    "basic": basic_chain,
    "memory": memory_chain,
    "retriever": retriever_chain,
}

def create_chain(chain_type: str = 'basic'):
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
        self.chains['test'] = create_chain(chain_type='basic')
        self.chains['general'] = create_chain(chain_type='memory')
        self.chains['knowledge'] = create_chain(chain_type='retriever')
    
    def get_chain(self, conversation_type: str = 'getneral'):
        return self.chains[conversation_type]