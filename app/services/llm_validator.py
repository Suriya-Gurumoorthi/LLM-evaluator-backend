"""Service for validating LLM API keys."""

import requests
from typing import Optional, Dict
from app.schemas.prompt_management import APIKeyValidationResponse


class LLMValidator:
    """Service for validating API keys for different LLM providers."""

    # Model IDs (match frontend and llm_calls.py) -> provider
    MODEL_TO_PROVIDER: Dict[str, str] = {
        "gemini_1_5_flash": "google",
        "gemini_2_5_flash": "google",
        "gemini_2_5_flash_lite": "google",
        "mistral": "mistral",
        "deepseek": "deepseek",
        "openai_gpt4_mini": "openai",
        "openai_gpt5_mini": "openai",
    }

    # Frontend/snake_case model ID -> API model name (for provider APIs that need it)
    MODEL_TO_GOOGLE_API_NAME: Dict[str, str] = {
        "gemini_1_5_flash": "gemini-1.5-flash",
        "gemini_2_5_flash": "gemini-2.5-flash",
        "gemini_2_5_flash_lite": "gemini-2.5-flash-lite",
    }

    def get_provider(self, model_id: str) -> Optional[str]:
        """Get the provider for a given model ID."""
        return self.MODEL_TO_PROVIDER.get(model_id.lower().strip())
    
    async def validate_api_key(
        self, 
        model_id: str, 
        api_key: str
    ) -> APIKeyValidationResponse:
        """
        Validate an API key for a given LLM model.
        
        Args:
            model_id: The LLM model identifier (e.g., 'gpt-4', 'claude-3-opus')
            api_key: The API key to validate
            
        Returns:
            APIKeyValidationResponse with validation result
        """
        provider = self.get_provider(model_id)
        
        if not provider:
            return APIKeyValidationResponse(
                is_valid=False,
                message=f"Unknown model: {model_id}. Supported: {', '.join(self.MODEL_TO_PROVIDER.keys())}",
                provider=None
            )
        
        try:
            if provider == "openai":
                return await self._validate_openai_key(model_id, api_key)
            elif provider == "google":
                return await self._validate_google_key(model_id, api_key)
            elif provider == "mistral":
                return await self._validate_mistral_key(api_key)
            elif provider == "deepseek":
                return await self._validate_deepseek_key(api_key)
            else:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message=f"Unsupported provider: {provider}",
                    provider=provider
                )
        except Exception as e:
            return APIKeyValidationResponse(
                is_valid=False,
                message=f"Error validating API key: {str(e)}",
                provider=provider
            )
    
    async def _validate_openai_key(
        self, 
        model_id: str, 
        api_key: str
    ) -> APIKeyValidationResponse:
        """Validate OpenAI API key by making a simple API call."""
        try:
            # Use OpenAI API to list models (lightweight call)
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                # Check if the requested model is available
                models = response.json().get("data", [])
                model_ids = [model.get("id") for model in models]
                
                # Normalize model_id for comparison
                normalized_model = model_id.lower()
                is_model_available = any(
                    normalized_model in model_id.lower() or model_id.lower() in model_id.lower()
                    for model_id in model_ids
                )
                
                if is_model_available or normalized_model in ["gpt-4", "gpt-3.5-turbo"]:
                    return APIKeyValidationResponse(
                        is_valid=True,
                        message=f"API key is valid. Model {model_id} is available.",
                        provider="openai"
                    )
                else:
                    return APIKeyValidationResponse(
                        is_valid=True,
                        message=f"API key is valid, but model {model_id} may not be available in your account.",
                        provider="openai"
                    )
            elif response.status_code == 401:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message="Invalid API key. Please check your OpenAI API key.",
                    provider="openai"
                )
            else:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message=f"API key validation failed with status {response.status_code}",
                    provider="openai"
                )
        except requests.exceptions.RequestException as e:
            return APIKeyValidationResponse(
                is_valid=False,
                message=f"Failed to connect to OpenAI API: {str(e)}",
                provider="openai"
            )
    
    async def _validate_anthropic_key(
        self, 
        model_id: str, 
        api_key: str
    ) -> APIKeyValidationResponse:
        """Validate Anthropic API key by making a simple API call."""
        try:
            # Use Anthropic API to make a minimal message call
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            
            # Minimal payload for validation
            payload = {
                "model": model_id,
                "max_tokens": 1,
                "messages": [
                    {"role": "user", "content": "test"}
                ]
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return APIKeyValidationResponse(
                    is_valid=True,
                    message=f"API key is valid. Model {model_id} is available.",
                    provider="anthropic"
                )
            elif response.status_code == 401:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message="Invalid API key. Please check your Anthropic API key.",
                    provider="anthropic"
                )
            elif response.status_code == 404:
                return APIKeyValidationResponse(
                    is_valid=True,
                    message=f"API key is valid, but model {model_id} may not be available.",
                    provider="anthropic"
                )
            else:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                return APIKeyValidationResponse(
                    is_valid=False,
                    message=f"API key validation failed: {error_msg}",
                    provider="anthropic"
                )
        except requests.exceptions.RequestException as e:
            return APIKeyValidationResponse(
                is_valid=False,
                message=f"Failed to connect to Anthropic API: {str(e)}",
                provider="anthropic"
            )
    
    async def _validate_google_key(
        self,
        model_id: str,
        api_key: str
    ) -> APIKeyValidationResponse:
        """Validate Google API key by making a simple API call."""
        # Normalize key: remove all whitespace (handles paste with newlines/spaces)
        api_key = "".join(api_key.split())
        if not api_key:
            return APIKeyValidationResponse(
                is_valid=False,
                message="API key is empty after removing spaces. Paste your key without extra spaces.",
                provider="google",
            )
        api_model = self.MODEL_TO_GOOGLE_API_NAME.get(
            model_id.lower().strip(), "gemini-1.5-flash"
        )
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{api_model}:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "test"
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": 1
                }
            }
            
            response = requests.post(
                url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return APIKeyValidationResponse(
                    is_valid=True,
                    message=f"API key is valid. Model {api_model} is available.",
                    provider="google"
                )
            elif response.status_code == 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "Invalid request")
                
                # Check if it's an API key issue or model issue
                if "API key" in error_msg or "permission" in error_msg.lower():
                    hint = (
                        " Get a key at https://aistudio.google.com/app/apikey and paste it with no extra spaces."
                    )
                    return APIKeyValidationResponse(
                        is_valid=False,
                        message=f"Invalid API key or insufficient permissions: {error_msg}.{hint}",
                        provider="google"
                    )
                else:
                    return APIKeyValidationResponse(
                        is_valid=True,
                        message=f"API key appears valid, but model {api_model} may not be available: {error_msg}",
                        provider="google"
                    )
            elif response.status_code == 401 or response.status_code == 403:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message="Invalid API key. Please check your Google API key.",
                    provider="google"
                )
            else:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message=f"API key validation failed with status {response.status_code}",
                    provider="google"
                )
        except requests.exceptions.RequestException as e:
            return APIKeyValidationResponse(
                is_valid=False,
                message=f"Failed to connect to Google API: {str(e)}",
                provider="google"
            )

    async def _validate_mistral_key(self, api_key: str) -> APIKeyValidationResponse:
        """Validate Mistral API key with a minimal chat request."""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "mistral-small-latest",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1,
            }
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10,
            )
            if response.status_code == 200:
                return APIKeyValidationResponse(
                    is_valid=True,
                    message="API key is valid. Mistral is available.",
                    provider="mistral",
                )
            elif response.status_code == 401:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message="Invalid API key. Please check your Mistral API key.",
                    provider="mistral",
                )
            else:
                err = response.json() if response.text else {}
                msg = err.get("message", err.get("error", response.text or f"Status {response.status_code}"))
                return APIKeyValidationResponse(
                    is_valid=False,
                    message=f"Mistral API: {msg}",
                    provider="mistral",
                )
        except requests.exceptions.RequestException as e:
            return APIKeyValidationResponse(
                is_valid=False,
                message=f"Failed to connect to Mistral API: {str(e)}",
                provider="mistral",
            )

    async def _validate_deepseek_key(self, api_key: str) -> APIKeyValidationResponse:
        """Validate DeepSeek API key (OpenAI-compatible) with a minimal completion."""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1,
            }
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10,
            )
            if response.status_code == 200:
                return APIKeyValidationResponse(
                    is_valid=True,
                    message="API key is valid. DeepSeek is available.",
                    provider="deepseek",
                )
            elif response.status_code == 401:
                return APIKeyValidationResponse(
                    is_valid=False,
                    message="Invalid API key. Please check your DeepSeek API key.",
                    provider="deepseek",
                )
            else:
                err = response.json() if response.text else {}
                msg = err.get("message", err.get("error", response.text or f"Status {response.status_code}"))
                return APIKeyValidationResponse(
                    is_valid=False,
                    message=f"DeepSeek API: {msg}",
                    provider="deepseek",
                )
        except requests.exceptions.RequestException as e:
            return APIKeyValidationResponse(
                is_valid=False,
                message=f"Failed to connect to DeepSeek API: {str(e)}",
                provider="deepseek",
            )


# Singleton instance
llm_validator = LLMValidator()
