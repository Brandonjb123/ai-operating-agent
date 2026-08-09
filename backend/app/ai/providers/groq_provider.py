import os
from app.ai.llm_provider import LLMProvider
from groq import Groq

class GroqProvider(LLMProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required")
        self.client = Groq(api_key=self.api_key)

    def complete(self, prompt: str, **kwargs) -> dict:
        try:
            # Parameter default bisa diambil dari kwargs atau konfigurasi
            model = kwargs.get("model", "llama3-8b-8192")
            temperature = kwargs.get("temperature", 0.7)
            max_tokens = kwargs.get("max_tokens", 4096)

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # Ambil konten respons pertama
            content = response.choices[0].message.content
            return {
                "success": True,
                "response": content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                "model": model,
            }
        except Exception as e:
            # Log traceback ke aplikasi log (tidak dikembalikan)
            # Untuk sekarang kita gunakan print, nanti bisa diganti logging
            print(f"GroqProvider error: {str(e)}")
            return {
                "success": False,
                "error": "LLM provider failed to process request",
            }