from langchain.prompts import PromptTemplate

from langchain_core.runnables import ConfigurableField

def chat_basic_template(template=True) -> any:
    prompt = """
    The following is a friendly conversation between a human and an AI. 
    The AI is talkative and provides lots of specific details from its context. 
    If the AI does not know the answer to a question, it truthfully says it does not know.
    {input}
    """

    return PromptTemplate.from_template(template=prompt) if template else prompt


def chat_memory_template(template=True) -> any:
    prompt = """ 
    ###Instruction
    The following is a friendly conversation between a human and an AI. 
    The AI is talkative and provides lots of specific details from its context. 
    If the AI does not know the answer to a question, it truthfully says it does not know.
    ###History conversation:
    {chat_history}
    ###Current conversation:
    {input}
    """

    return PromptTemplate.from_template(template=prompt) if template else prompt

def get_configurable_template() -> any:
    prompt_template = chat_basic_template()

    return prompt_template.configurable_alternatives(
        ConfigurableField(id="prompt"),
        default_key="basic",
        memory=chat_memory_template()
    )