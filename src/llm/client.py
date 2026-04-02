"""
Unified LLM call interface. Supports OpenAI and DeepSeek (via env OPENAI_API_KEY or DEEPSEEK_API_KEY).
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
    if temperature <= 0.2:
        h = _cache_prompt_hash(prompt)
        hit = _cache_get(h)
        if hit is not None:
            return hit

    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()

    if openai_key:
        out = _call_openai(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
    elif deepseek_key:
        out = _call_deepseek(prompt, max_tokens=max_tokens, temperature=temperature, model=model)
    else:
        out = None

    if out is not None and temperature <= 0.2:
        _cache_set(_cache_prompt_hash(prompt), out)
    return out


def _call_openai(
    prompt: str,
    *,
    max_tokens: int = 256,
    temperature: float = 0.4,
    model: str | None = None,
) -> str | None:
    try:
        import openai
        from openai import APITimeoutError

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
    except APITimeoutError as e:
        logger.warning("OpenAI LLM request timed out: %s", e)
        return None
    except httpx.TimeoutException as e:
        logger.warning("OpenAI LLM HTTP timeout: %s", e)
        return None
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
        from openai import APITimeoutError

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
    except APITimeoutError as e:
        logger.warning("DeepSeek LLM request timed out: %s", e)
        return None
    except httpx.TimeoutException as e:
        logger.warning("DeepSeek LLM HTTP timeout: %s", e)
        return None
    except Exception:
        return None


def llm_completion_parallel(
    prompts: list[tuple[str, dict]],
    max_workers: int = 3,
) -> list[str | None]:
    if not prompts:
        return []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(lambda t: llm_completion(t[0], **t[1]), prompts))


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
        from openai import APITimeoutError

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
    except APITimeoutError as e:
        logger.warning("OpenAI LLM stream timed out: %s", e)
    except httpx.TimeoutException as e:
        logger.warning("OpenAI LLM stream HTTP timeout: %s", e)
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
        from openai import APITimeoutError

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
    except APITimeoutError as e:
        logger.warning("DeepSeek LLM stream timed out: %s", e)
    except httpx.TimeoutException as e:
        logger.warning("DeepSeek LLM stream HTTP timeout: %s", e)
    except Exception:
        pass
