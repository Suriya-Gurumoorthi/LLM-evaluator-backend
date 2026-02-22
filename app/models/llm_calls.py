"""
Seven LLM call functions. Each function calls one fixed model.
No .env usage: model IDs are hardcoded; API keys are passed in by the caller.
All functions: (formatted_messages, system_prompt, ..., api_key) -> (response_text, input_tokens, output_tokens).
"""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# Default model IDs (hardcoded, not from .env)
_MODEL_GEMINI_1_5_FLASH = "gemini-1.5-flash"
_MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash"
_MODEL_GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"
_MODEL_MISTRAL_SMALL = "mistral-small-latest"
_MODEL_DEEPSEEK_CHAT = "deepseek-chat"
_MODEL_OPENAI_GPT4_MINI = "gpt-4.1-mini"
_MODEL_OPENAI_GPT5_MINI = "gpt-5-mini"

_genai_clients: dict = {}
_mistral_clients: dict = {}
_deepseek_clients: dict = {}
_openai_clients: dict = {}


def _gemini_call(
    model_id: str,
    api_key: str,
    formatted_messages: list,
    system_prompt: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    from google.genai import types
    from google.genai import Client
    if api_key not in _genai_clients:
        _genai_clients[api_key] = Client(api_key=api_key)
    client = _genai_clients[api_key]
    parts = []
    for msg in formatted_messages:
        role = (msg.get("role") or "user").lower()
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role == "system":
            system_prompt = f"{system_prompt}\n{content}".strip() if system_prompt else content
        else:
            parts.append(content)
    user_content = "\n\n".join(parts) if parts else ""
    if not user_content:
        raise ValueError("No user content in formatted_messages for Gemini")
    config = types.GenerateContentConfig(
        system_instruction=system_prompt or None,
        max_output_tokens=max_tokens,
        temperature=temperature,
    )
    response = client.models.generate_content(
        model=model_id,
        contents=user_content,
        config=config,
    )
    response_text = (response.text or "").strip()
    if not response_text:
        raise ValueError("Empty response text from Gemini API")
    usage = getattr(response, "usage_metadata", None)
    input_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
    output_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0
    return response_text, input_tokens, output_tokens


def gemini_1_5_flash_call(
    formatted_messages: list,
    system_prompt: str,
    api_key: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    """Call Gemini 1.5 Flash. Returns (response_text, input_tokens, output_tokens)."""
    return _gemini_call(
        _MODEL_GEMINI_1_5_FLASH,
        api_key,
        formatted_messages,
        system_prompt,
        max_tokens,
        temperature,
    )


def gemini_2_5_flash_call(
    formatted_messages: list,
    system_prompt: str,
    api_key: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    """Call Gemini 2.5 Flash. Returns (response_text, input_tokens, output_tokens)."""
    return _gemini_call(
        _MODEL_GEMINI_2_5_FLASH,
        api_key,
        formatted_messages,
        system_prompt,
        max_tokens,
        temperature,
    )


def gemini_2_5_flash_lite_call(
    formatted_messages: list,
    system_prompt: str,
    api_key: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    """Call Gemini 2.5 Flash Lite. Returns (response_text, input_tokens, output_tokens)."""
    return _gemini_call(
        _MODEL_GEMINI_2_5_FLASH_LITE,
        api_key,
        formatted_messages,
        system_prompt,
        max_tokens,
        temperature,
    )


def mistral_call(
    formatted_messages: list,
    system_prompt: str,
    api_key: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    """Call Mistral (mistral-small-latest). Returns (response_text, input_tokens, output_tokens)."""
    if api_key not in _mistral_clients:
        from mistralai import Mistral
        _mistral_clients[api_key] = Mistral(api_key=api_key)
    client = _mistral_clients[api_key]
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for msg in formatted_messages:
        role = (msg.get("role") or "user").lower()
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role not in {"user", "assistant", "system"}:
            role = "user"
        messages.append({"role": role, "content": content})
    if not messages:
        raise ValueError("No messages provided for Mistral")
    chat_response = client.chat.complete(
        model=_MODEL_MISTRAL_SMALL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    if not getattr(chat_response, "choices", None) or len(chat_response.choices) == 0:
        raise ValueError("Empty response from Mistral API")
    content = getattr(chat_response.choices[0].message, "content", None)
    if content is None:
        raise ValueError("Empty content from Mistral API")
    if isinstance(content, str):
        response_text = content.strip()
    elif isinstance(content, list):
        response_text = ""
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                response_text = (part.get("text") or "").strip()
                break
    else:
        response_text = ""
    if not response_text:
        raise ValueError("Empty response text from Mistral API")
    usage = getattr(chat_response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", 0) or getattr(usage, "input_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "completion_tokens", 0) or getattr(usage, "output_tokens", 0) if usage else 0
    return response_text, input_tokens, output_tokens


def deepseek_call(
    formatted_messages: list,
    system_prompt: str,
    api_key: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    """Call DeepSeek (deepseek-chat). Returns (response_text, input_tokens, output_tokens)."""
    if api_key not in _deepseek_clients:
        from openai import OpenAI
        _deepseek_clients[api_key] = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    client = _deepseek_clients[api_key]
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for msg in formatted_messages:
        role = (msg.get("role") or "user").lower()
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        if role not in {"user", "assistant", "system"}:
            role = "user"
        messages.append({"role": role, "content": content})
    if not messages:
        raise ValueError("No messages provided for DeepSeek")
    response = client.chat.completions.create(
        model=_MODEL_DEEPSEEK_CHAT,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=False,
    )
    if not response.choices:
        raise ValueError("Empty response from DeepSeek API")
    msg = response.choices[0].message
    response_text = (msg.content or "").strip()
    if not response_text and getattr(msg, "reasoning_content", None):
        response_text = (msg.reasoning_content or "").strip()
    if not response_text:
        raise ValueError("Empty response text from DeepSeek API")
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0
    return response_text, input_tokens, output_tokens


def _openai_call(
    model_id: str,
    api_key: str,
    formatted_messages: list,
    system_prompt: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    if api_key not in _openai_clients:
        from openai import OpenAI
        _openai_clients[api_key] = OpenAI(api_key=api_key)
    client = _openai_clients[api_key]
    input_parts = []
    if system_prompt:
        input_parts.append(f"System: {system_prompt}")
    for msg in formatted_messages:
        role = (msg.get("role") or "user").lower()
        content = (msg.get("content") or "").strip()
        if not content:
            continue
        input_parts.append(f"{role.capitalize()}: {content}")
    if not input_parts:
        raise ValueError("No messages provided for OpenAI")
    input_text = "\n\n".join(input_parts)
    response = client.responses.create(model=model_id, input=input_text)
    if not hasattr(response, "output_text"):
        raise ValueError("OpenAI API response missing output_text attribute")
    response_text = response.output_text
    if response_text is None:
        raise ValueError("OpenAI API returned None for output_text")
    response_text = response_text.strip() if isinstance(response_text, str) else str(response_text).strip()
    if not response_text:
        raise ValueError("OpenAI API returned empty response text")
    input_tokens = getattr(response, "input_tokens", 0) or 0
    output_tokens = getattr(response, "output_tokens", 0) or 0
    if hasattr(response, "usage"):
        input_tokens = getattr(response.usage, "prompt_tokens", input_tokens)
        output_tokens = getattr(response.usage, "completion_tokens", output_tokens)
    return response_text, input_tokens, output_tokens


def openai_gpt4_mini_call(
    formatted_messages: list,
    system_prompt: str,
    api_key: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    """Call OpenAI GPT 4.1 mini. Returns (response_text, input_tokens, output_tokens)."""
    return _openai_call(
        _MODEL_OPENAI_GPT4_MINI,
        api_key,
        formatted_messages,
        system_prompt,
        max_tokens,
        temperature,
    )


def openai_gpt5_mini_call(
    formatted_messages: list,
    system_prompt: str,
    api_key: str,
    max_tokens: int = 1000,
    temperature: float = 0.1,
) -> Tuple[str, int, int]:
    """Call OpenAI GPT 5 mini. Returns (response_text, input_tokens, output_tokens)."""
    return _openai_call(
        _MODEL_OPENAI_GPT5_MINI,
        api_key,
        formatted_messages,
        system_prompt,
        max_tokens,
        temperature,
    )
