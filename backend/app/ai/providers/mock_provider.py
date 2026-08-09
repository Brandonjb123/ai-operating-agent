"""
Mock LLM Provider untuk testing success path.
Hanya digunakan saat verifikasi, bukan untuk production.
"""

from app.ai.llm_provider import LLMProvider


class MockLLMProvider(LLMProvider):
    """Provider palsu yang selalu mengembalikan respons sukses."""

    def complete(self, prompt: str, **kwargs) -> dict:
        return {
            "success": True,
            "response": f"Mock response for prompt: {prompt[:50]}...",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30,
            },
            "model": kwargs.get("model", "mock-model"),
        }