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
    The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    ###History conversation:
    {chat_history}
    ###Current conversation:
    {input}
    """

    return PromptTemplate.from_template(template=prompt) if template else prompt

# NOTE :: 샘플 템플릿이기 때문에 프로젝트 상황에 따라 자유롭게 변경하여 사용
def multi_turn_template(template=True) -> any:
    prompt = """
    지게차와 고소장비 관련된 문제현상에 대해 입력된 문장에서 다음 정보를 추출해주세요. \
    추출된 정보를 아래 형식의 JSON으로 출력해주세요.
    
    << FORMATTING >>
    Return a markdown code snippet with a JSON object formatted to look like:
    ```json
        {{{{
        \"brand_name\": str \\ 제조사명 (예: TOYOTA, DOOSAN)
        \"model_name\": str \\ 모델 유형 (예: 7FBR10_18, D20/25/30/33S(SE)_7)
        \"error_code\": str \\ 에러 코드 (예: Error Code F7, Error Code A4, Error Code A6, Error Code A8, Error Code 51-1, Error Code 51-3, Error Code 54-1, Error Code 64-1, Error Code 71-1, Error Code 72-1, Error Code 74-1)
        }}}}
    ```

    REMEMBER: "brand_name" MUST be a name of brand, brand name are TOYOTA, DOOSAN. 
    REMEMBER: "model_name" MUST be a name of model, model name are 7FBR10_18, D20/25/30/33S(SE)_7. 
    REMEMBER: "error_code" MUST be a name of error code are Error Code F7, Error Code A4, Error Code A6, Error Code A8, Error Code 51-1, Error Code 51-3, Error Code 54-1, Error Code 64-1, Error Code 71-1, Error Code 72-1, Error Code 74-1. 
    REMEMBER: 입력된 문장에서 명확하게 추출할 정보가 없을 경우 null을 반환하세요.

    << INPUT >> {input} \n\n << OUTPUT (remember to include the ```json)>>

    REMEMBER: Read request again {input}
    """

    return PromptTemplate.from_template(template=prompt) if template else prompt

def get_configurable_template() -> any:
    prompt_template = chat_basic_template()

    return prompt_template.configurable_alternatives(
        ConfigurableField(id="prompt"),
        default_key="basic",
        memory=chat_memory_template(),
        multi_turn=multi_turn_template()
    )