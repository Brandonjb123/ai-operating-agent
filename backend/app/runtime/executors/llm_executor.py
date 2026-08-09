from ..step_executor import StepExecutor
from ..execution_context import ExecutionContext
from ..step_result import StepResult
from ...ai.llm_provider import LLMProvider

class LLMExecutor(StepExecutor):
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def execute(self, step: dict, context: ExecutionContext) -> StepResult:
        # Ambil config
        config = step.get("config", {})
        prompt_template = config.get("prompt", "")
        # Isi template dengan variabel dari context
        prompt = prompt_template.format(**context.variables) if prompt_template else ""

        # Ambil parameter model dari config, fallback ke default
        model = config.get("model")
        temperature = config.get("temperature")
        max_tokens = config.get("max_tokens")

        kwargs = {}
        if model:
            kwargs["model"] = model
        if temperature is not None:
            kwargs["temperature"] = temperature
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        # Panggil provider
        result = self.llm_provider.complete(prompt, **kwargs)

        if result.get("success"):
            return StepResult(
                step_id=step["id"],
                success=True,
                output={"response": result.get("response")},
                metadata={
                    "model": result.get("model"),
                    "usage": result.get("usage"),
                }
            )
        else:
            return StepResult(
                step_id=step["id"],
                success=False,
                error=result.get("error", "Unknown error"),
                metadata={}
            )