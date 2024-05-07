import sys
from typing import Any, Dict, Iterator
from llmuses.perf.openai.stream_base import OpenaiPluginBase

class PerfPlugin(OpenaiPluginBase):
    def __init__(self, model_path: str):
        super().__init__(model_path)

    def build_request(self,
                      model: str,
                      prompt: str = None,
                      dataset: str = None,
                      max_length: int = sys.maxsize,
                      min_length: int = 0,
                      **kwargs: Any) -> Iterator[Dict]:
        if prompt is not None:
            messages = [{'role': 'user', 'content': prompt}]
            yield {
                "model": model,
                "messages": messages,
                "stream": True,
                **kwargs}
        elif dataset is not None:
            for item in self.dataset_json_list(dataset):
                instruction = item['instruction']
                if len(instruction) > min_length and len(instruction) < max_length:
                    messages = [{'role': 'user', 'content': instruction}]
                    yield {
                        "model": model,
                        "messages": messages,
                        "stream": True,
                        "skip_special_tokens": False,
                        "stop": ["<|im_end|>"],
                        **kwargs}
        else:
            raise Exception('prompt or dataset is required!')

    def parse_responses(self, responses, request: Any = None, **kwargs) -> Dict:
        return super().parse_responses(responses, request, **kwargs)
        
        
