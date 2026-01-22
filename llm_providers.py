"""LLM provider implementations for multiple AI services."""

import os
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable

from openai import OpenAI, APIError, RateLimitError, APIConnectionError

from config import (
    MAX_TOKENS,
    RETRY_ATTEMPTS,
    RETRY_DELAY,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL
)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Generate content from prompts."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get provider name."""
        pass


class DeepSeekProvider(LLMProvider):
    """DeepSeek LLM provider implementation."""
    
    def __init__(self):
        """Initialize DeepSeek provider."""
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL
        self.model = DEEPSEEK_MODEL
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Generate content using DeepSeek API."""
        last_error = None
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                if progress_callback:
                    progress_callback(attempt / RETRY_ATTEMPTS * 0.3)
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    stream=False,
                    max_tokens=MAX_TOKENS,
                    temperature=0.7,
                )
                
                if progress_callback:
                    progress_callback(0.8)
                
                return response.choices[0].message.content
                
            except (RateLimitError, APIConnectionError, APIError) as e:
                last_error = e
                if attempt < RETRY_ATTEMPTS - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    time.sleep(wait_time)
        
        raise ValueError(f"DeepSeek API failed after {RETRY_ATTEMPTS} attempts: {last_error}")
    
    def get_name(self) -> str:
        """Get provider name."""
        return "DeepSeek"


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider implementation."""
    
    def __init__(self, model: str = "gpt-4"):
        """Initialize OpenAI provider."""
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Generate content using OpenAI API."""
        last_error = None
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                if progress_callback:
                    progress_callback(attempt / RETRY_ATTEMPTS * 0.3)
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=MAX_TOKENS,
                    temperature=0.7,
                )
                
                if progress_callback:
                    progress_callback(0.8)
                
                return response.choices[0].message.content
                
            except (RateLimitError, APIConnectionError, APIError) as e:
                last_error = e
                if attempt < RETRY_ATTEMPTS - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    time.sleep(wait_time)
        
        raise ValueError(f"OpenAI API failed after {RETRY_ATTEMPTS} attempts: {last_error}")
    
    def get_name(self) -> str:
        """Get provider name."""
        return f"OpenAI ({self.model})"


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider implementation."""
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize Anthropic provider."""
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.model = model
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Generate content using Anthropic API."""
        last_error = None
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                if progress_callback:
                    progress_callback(attempt / RETRY_ATTEMPTS * 0.3)
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=MAX_TOKENS,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                )
                
                if progress_callback:
                    progress_callback(0.8)
                
                return response.content[0].text
                
            except Exception as e:
                last_error = e
                if attempt < RETRY_ATTEMPTS - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    time.sleep(wait_time)
        
        raise ValueError(f"Anthropic API failed after {RETRY_ATTEMPTS} attempts: {last_error}")
    
    def get_name(self) -> str:
        """Get provider name."""
        return f"Anthropic ({self.model})"


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider implementation."""
    
    def __init__(self, model: str = "llama3.1", base_url: str = "http://localhost:11434"):
        """Initialize Ollama provider."""
        self.model = model
        self.base_url = base_url
        
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("requests package not installed. Run: pip install requests")
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Generate content using Ollama local API."""
        last_error = None
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                if progress_callback:
                    progress_callback(attempt / RETRY_ATTEMPTS * 0.3)
                
                response = self.requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"System: {system_prompt}\n\nUser: {user_prompt}",
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": MAX_TOKENS,
                        }
                    },
                    timeout=300
                )
                
                response.raise_for_status()
                
                if progress_callback:
                    progress_callback(0.8)
                
                return response.json()["response"]
                
            except Exception as e:
                last_error = e
                if attempt < RETRY_ATTEMPTS - 1:
                    wait_time = RETRY_DELAY * (attempt + 1)
                    time.sleep(wait_time)
        
        raise ValueError(f"Ollama API failed after {RETRY_ATTEMPTS} attempts: {last_error}")
    
    def get_name(self) -> str:
        """Get provider name."""
        return f"Ollama ({self.model})"


def create_provider(provider_name: str, **kwargs) -> LLMProvider:
    """
    Factory function to create LLM provider instances.
    
    Args:
        provider_name: Name of the provider ('deepseek', 'openai', 'anthropic', 'ollama')
        **kwargs: Additional provider-specific arguments
        
    Returns:
        LLMProvider instance
        
    Raises:
        ValueError: If provider name is not recognized
    """
    provider_name = provider_name.lower()
    
    providers = {
        'deepseek': DeepSeekProvider,
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'ollama': OllamaProvider,
    }
    
    if provider_name not in providers:
        available = ', '.join(providers.keys())
        raise ValueError(f"Unknown provider: {provider_name}. Available: {available}")
    
    return providers[provider_name](**kwargs)


def get_available_providers() -> Dict[str, str]:
    """
    Get list of available providers with their descriptions.
    
    Returns:
        Dictionary of provider names to descriptions
    """
    return {
        'deepseek': 'DeepSeek AI (default, cost-effective)',
        'openai': 'OpenAI GPT-4 (requires OPENAI_API_KEY)',
        'anthropic': 'Anthropic Claude (requires ANTHROPIC_API_KEY)',
        'ollama': 'Ollama local models (requires Ollama running locally)',
    }
