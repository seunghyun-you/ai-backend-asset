import os
import boto3
from collections import OrderedDict

from langchain_aws import ChatBedrock
from langchain_core.runnables import ConfigurableField

def get_bedrock_client():
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-west-2"),
        endpoint_url=os.environ.get("BEDROCK_ENDPOINT_URL", "https://bedrock-runtime.us-west-2.amazonaws.com"),
        verify=False,
    )

def get_bedrock_models_Information(model=None, temperature=0.0, topP=0.9, max_tokens=8000):
    claude_model_kwargs = {
        "max_tokens": max_tokens,
        "stop_sequences": ["\\n\\nHuman:", "\\nHuman:", "Human:"],
        "temperature": temperature,
        "top_k": 100,
        "top_p": topP,
        "anthropic_version": "bedrock-2023-05-31"
    }

    claude_v3_model_kwargs = {
        "max_tokens": max_tokens,
        "stop_sequences": ["\\n\\nHuman:", "\\nHuman:", "Human:"],
        "temperature": temperature,
        "top_k": 100,
        "top_p": topP,
        "anthropic_version": "bedrock-2023-05-31"
    }

    ai21_model_kwargs = {
        "maxTokens": max_tokens,
        "stopSequences": ['\nHuman:'],
        "temperature": temperature,
        "topP": topP
    }

    titan_model_kwargs = {
        "maxTokenCount": max_tokens,
        "stopSequences": [],
        "temperature": temperature,
        "topP": topP
    }

    mixtral_8_7_model_kwargs = {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_k": 100,
        "top_p": topP,
    }

    amazon_titan_tg1_large_model_id = "amazon.titan-tg1-large"
    ai21_j2_mid_model_id = "ai21.j2-mid"
    ai21_j2_jumbo_instruct_model_id = "ai21.j2-jumbo-instruct"
    anthropic_claude_instance_v1_model_id = "anthropic.claude-instant-v1"
    anthropic_claude_v1_model_id = "anthropic.claude-v1"
    anthropic_claude_v2_model_id = "anthropic.claude-v2"
    anthropic_claude_v2_1_model_id = "anthropic.claude-v2:1"
    anthropic_claude_v3_sonnet_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    anthropic_claude_v3_haiku_model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    anthropic_claude_v3_opus_model_id = "anthropic.claude-3-opus-20240229-v1:0"
    anthropic_claude_v3_5_sonnet_model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    mistral_mixtral_8_7_model_id = "mistral.mixtral-8x7b-instruct-v0:1"

    amazon_titan_tg1_large_model = (amazon_titan_tg1_large_model_id, titan_model_kwargs)
    ai21_j2_mid = (ai21_j2_mid_model_id, ai21_model_kwargs)
    ai21_j2_jumbo_instruct = (ai21_j2_jumbo_instruct_model_id, ai21_model_kwargs)
    anthropic_claude_instance_v1 = (anthropic_claude_instance_v1_model_id, claude_model_kwargs)
    anthropic_claude_v1 = (anthropic_claude_v1_model_id, claude_model_kwargs)
    anthropic_claude_v2 = (anthropic_claude_v2_model_id, claude_model_kwargs)
    anthropic_claude_v2_1 = (anthropic_claude_v2_1_model_id, claude_model_kwargs)
    anthropic_claude_v3_sonnet = (anthropic_claude_v3_sonnet_model_id, claude_v3_model_kwargs)
    anthropic_claude_v3_haiku = (anthropic_claude_v3_haiku_model_id, claude_v3_model_kwargs)
    anthropic_claude_v3_opus = (anthropic_claude_v3_opus_model_id, claude_v3_model_kwargs)
    anthropic_claude_v3_5_sonnet = (anthropic_claude_v3_5_sonnet_model_id, claude_v3_model_kwargs)
    mistral_mixtral_8_7 = (mistral_mixtral_8_7_model_id, mixtral_8_7_model_kwargs)

    models = OrderedDict({'AI21 Jurrasic-2 Mid': ai21_j2_mid,
                          'AI21 Jurrasic-2 Ultra': ai21_j2_jumbo_instruct,
                          'Amazon Titan Large': amazon_titan_tg1_large_model,
                          'Anthropic Claude Instant v1': anthropic_claude_instance_v1,
                          'Anthropic Claude v1': anthropic_claude_v1,
                          'Anthropic Claude v2': anthropic_claude_v2,
                          'Anthropic Claude v2.1': anthropic_claude_v2_1,
                          'Anthropic Claude v3 Sonnet': anthropic_claude_v3_sonnet,
                          'Anthropic Claude v3 Haiku': anthropic_claude_v3_haiku,
                          'Anthropic Claude v3 Opus': anthropic_claude_v3_opus,
                          'Anthropic Claude v3.5 Sonnet': anthropic_claude_v3_5_sonnet,
                          'Mistral Mixtral 8x7 Instruct': mistral_mixtral_8_7
                          })

    if model:
        return models[model]

    return models

def get_bedrock_model(model_name='Anthropic Claude v3 Haiku', model_params=None) -> ChatBedrock:
    model_info = get_bedrock_models_Information(model_name)

    model_id = model_info[0]
    model_params = model_params if model_params is not None else model_info[1]
    bedrock_client = get_bedrock_client()

    return ChatBedrock(
        client=bedrock_client,
        model_id=model_id,
        model_kwargs=model_params,
    )

def get_configurable_llm():
    haiku = get_bedrock_model(model_name='Anthropic Claude v3 Haiku', model_params=None)

    return haiku.configurable_alternatives(
        ConfigurableField(id='llm'),
        default_key='haiku',
        opus=get_bedrock_model(model_name='Anthropic Claude v3 Opus', model_params=None),
        sonnet=get_bedrock_model(model_name='Anthropic Claude v3 Sonnet', model_params=None),
        sonnet35=get_bedrock_model(model_name='Anthropic Claude v3.5 Sonnet', model_params=None)
    )