"""Service for interacting with Google Gemini API."""

import requests
from typing import Optional, Dict, Any
import json


class GeminiClient:
    """Client for Google Gemini API."""
    
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
    
    async def generate_content(
        self,
        prompt: str,
        test_case_input: str,
        model: str = "gemini-pro"
    ) -> Dict[str, Any]:
        """
        Generate content using Gemini API for a test case.
        
        Args:
            prompt: The main prompt to evaluate
            test_case_input: The input for this specific test case
            model: Gemini model to use (default: gemini-pro)
            
        Returns:
            Dictionary with response data including generated text
        """
        # Construct the full prompt by combining the main prompt with test case input
        full_prompt = f"{prompt}\n\nInput: {test_case_input}"
        
        url = f"{self.BASE_URL}/{model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract the generated text
                candidates = data.get("candidates", [])
                if candidates and len(candidates) > 0:
                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if parts and len(parts) > 0:
                        generated_text = parts[0].get("text", "")
                        
                        return {
                            "success": True,
                            "generated_text": generated_text,
                            "full_response": data,
                            "model_used": model
                        }
                
                return {
                    "success": False,
                    "error": "No content generated in response",
                    "full_response": data
                }
            
            elif response.status_code == 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "Bad request")
                return {
                    "success": False,
                    "error": f"Bad request: {error_msg}",
                    "status_code": 400
                }
            
            elif response.status_code == 401 or response.status_code == 403:
                return {
                    "success": False,
                    "error": "Invalid API key or insufficient permissions",
                    "status_code": response.status_code
                }
            
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "status_code": response.status_code,
                    "response": response.text
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout - API took too long to respond"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    async def generate_batch(
        self,
        prompt: str,
        test_case_inputs: list[str],
        model: str = "gemini-pro"
    ) -> list[Dict[str, Any]]:
        """
        Generate content for multiple test cases sequentially.
        
        Args:
            prompt: The main prompt to evaluate
            test_case_inputs: List of test case inputs
            model: Gemini model to use
            
        Returns:
            List of response dictionaries for each test case
        """
        results = []
        
        for test_case_input in test_case_inputs:
            result = await self.generate_content(prompt, test_case_input, model)
            results.append(result)
        
        return results
