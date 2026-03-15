"""
Unified LLM call interface. Supports OpenAI and DeepSeek (via env OPENAI_API_KEY or DEEPSEEK_API_KEY).
"""

import os
from typing import Any, Iterator


def llm_completion(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> str | None:
    """
    Call LLM for completion. Tries OpenAI first if OPENAI_API_KEY is set,
    then DeepSeek if DEEPSEEK_API_KEY is set. Returns None on failure or missing key.
    """
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()

    if openai_key:
        return _call_openai(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
    if deepseek_key:
        return _call_deepseek(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
    return None


def _call_openai(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> str | None:
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model or "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        text = (response.choices[0].message.content or "").strip()
        return text or None
    except Exception:
        return None


def _call_deepseek(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> str | None:
    try:
        import openai
        # DeepSeek API is OpenAI-compatible
        client = openai.OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1",
        )
        response = client.chat.completions.create(
            model=model or "deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        text = (response.choices[0].message.content or "").strip()
        return text or None
    except Exception:
        return None


def llm_completion_stream(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> Iterator[str]:
    """Stream LLM completion token-by-token. Yields text deltas."""
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if openai_key:
        yield from _call_openai_stream(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
        return
    if deepseek_key:
        yield from _call_deepseek_stream(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
        return
    out = llm_completion(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
    if out:
        yield out


def _call_openai_stream(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> Iterator[str]:
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        stream = client.chat.completions.create(
            model=model or "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
        for chunk in stream:
            delta = (chunk.choices[0].delta.content or "") if chunk.choices else ""
            if delta:
                yield delta
    except Exception:
        pass


def _call_deepseek_stream(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> Iterator[str]:
    try:
        import openai
        client = openai.OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1",
        )
        stream = client.chat.completions.create(
            model=model or "deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
        for chunk in stream:
            delta = (chunk.choices[0].delta.content or "") if chunk.choices else ""
            if delta:
                yield delta
    except Exception:
        pass
