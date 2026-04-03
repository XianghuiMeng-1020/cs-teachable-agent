"""
Unified LLM call interface with fallback chain: DeepSeek → OpenAI → Qwen.
Tries each configured provider in order; falls back to the next on failure.
"""

import hashlib
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

import httpx

logger = logging.getLogger(__name__)

_CACHE_TTL_SEC = 300
_CACHE_MAX_ENTRIES = 200
_cache: dict[str, tuple[str, float]] = {}


def _llm_http_timeout() -> httpx.Timeout:
    return httpx.Timeout(30.0)


def _cache_prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def _cache_get(prompt_hash: str) -> str | None:
    now = time.time()
    item = _cache.get(prompt_hash)
    if item is None:
        return None
    response, ts = item
    if now - ts > _CACHE_TTL_SEC:
        del _cache[prompt_hash]
        return None
    del _cache[prompt_hash]
    _cache[prompt_hash] = (response, ts)
    return response


def _cache_set(prompt_hash: str, response: str) -> None:
    now = time.time()
    if prompt_hash in _cache:
        del _cache[prompt_hash]
    _cache[prompt_hash] = (response, now)
    while len(_cache) > _CACHE_MAX_ENTRIES:
        oldest = next(iter(_cache))
        del _cache[oldest]


# ---------------------------------------------------------------------------
# Provider registry: each entry is (env_var, call_fn, stream_fn, label)
# Order determines fallback priority.
# ---------------------------------------------------------------------------

def _providers():
    """Return list of available providers in fallback order."""
    providers = []
    if os.environ.get("DEEPSEEK_API_KEY", "").strip():
        providers.append(("deepseek", _call_deepseek, _call_deepseek_stream))
    if os.environ.get("OPENAI_API_KEY", "").strip():
        providers.append(("openai", _call_openai, _call_openai_stream))
    if os.environ.get("QWEN_API_KEY", "").strip():
        providers.append(("qwen", _call_qwen, _call_qwen_stream))
    return providers


def llm_completion(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> str | None:
    """
    Call LLM for completion with automatic fallback.
    Tries providers in order: DeepSeek → OpenAI → Qwen.
    """
    if temperature <= 0.2:
        h = _cache_prompt_hash(prompt)
        hit = _cache_get(h)
        if hit is not None:
            return hit

    for label, call_fn, _ in _providers():
        try:
            out = call_fn(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
            if out:
                if temperature <= 0.2:
                    _cache_set(_cache_prompt_hash(prompt), out)
                return out
        except Exception as e:
            logger.warning("LLM provider %s failed, trying next: %s", label, e)
            continue

    return None


def llm_completion_stream(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> Iterator[str]:
    """Stream LLM completion with automatic fallback."""
    for label, _, stream_fn in _providers():
        try:
            tokens = list(stream_fn(prompt, max_tokens=max_tokens, temperature=temperature, model=model))
            if tokens:
                yield from tokens
                return
        except Exception as e:
            logger.warning("LLM stream provider %s failed, trying next: %s", label, e)
            continue

    out = llm_completion(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
    if out:
        yield out


def llm_completion_parallel(
    prompts: list[tuple[str, dict]],
    max_workers: int = 3,
) -> list[str | None]:
    if not prompts:
        return []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(lambda t: llm_completion(t[0], **t[1]), prompts))


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------

def _call_openai(prompt, *, max_tokens=256, temperature=0.4, model=None):
    import openai
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        timeout=_llm_http_timeout(),
    )
    response = client.chat.completions.create(
        model=model or "gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    text = (response.choices[0].message.content or "").strip()
    return text or None


def _call_deepseek(prompt, *, max_tokens=256, temperature=0.4, model=None):
    import openai
    client = openai.OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        timeout=_llm_http_timeout(),
    )
    response = client.chat.completions.create(
        model=model or "deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    text = (response.choices[0].message.content or "").strip()
    return text or None


def _call_qwen(prompt, *, max_tokens=256, temperature=0.4, model=None):
    import openai
    client = openai.OpenAI(
        api_key=os.environ.get("QWEN_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        timeout=_llm_http_timeout(),
    )
    response = client.chat.completions.create(
        model=model or "qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    text = (response.choices[0].message.content or "").strip()
    return text or None


# ---------------------------------------------------------------------------
# Stream implementations
# ---------------------------------------------------------------------------

def _call_openai_stream(prompt, *, max_tokens=256, temperature=0.4, model=None) -> Iterator[str]:
    import openai
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        timeout=_llm_http_timeout(),
    )
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


def _call_deepseek_stream(prompt, *, max_tokens=256, temperature=0.4, model=None) -> Iterator[str]:
    import openai
    client = openai.OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        timeout=_llm_http_timeout(),
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


def _call_qwen_stream(prompt, *, max_tokens=256, temperature=0.4, model=None) -> Iterator[str]:
    import openai
    client = openai.OpenAI(
        api_key=os.environ.get("QWEN_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        timeout=_llm_http_timeout(),
    )
    stream = client.chat.completions.create(
        model=model or "qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )
    for chunk in stream:
        delta = (chunk.choices[0].delta.content or "") if chunk.choices else ""
        if delta:
            yield delta
