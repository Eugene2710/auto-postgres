from functools import lru_cache
from typing import Any,Optional

import openai
import requests as requests

from services.sql_prompt_formatter import SQLPrompt, SQLPromptFormatter
from settings import OPENAI_KEY

class OpenAICompletor:
    """
    A service responsible for sending a prompt to openai, to get results back
    - Used to send the SQLPrompt to openai, to get the SQL query to execute
    - Used to send the ResultPrompt to openai, to get the interpreted results
    """
    def __init__(self):
        # debugging
        """
        API Reference: https://platform.openai.com/docs/api-reference/chat/create
        """
        self.model = "gpt-3.5-turbo"    # The ai model we are using. TODO: get the ChatGPT model from the openai playground
        self.max_tokens = 1000          # Max tokens inclusive of the prompt + completion
        self.top_p = 0                  # 0 to 1. The higher it is, the more adventurous the model is.
        self.n = 1                      # completions to generate. we only want 1
        self.stream = False             # whether to stream back partial progress. set to False
        self.stop = ["#", ";"]          # if model encounters this token, it stops generating.

    @staticmethod
    def parse_completion(json: dict[str, Any]) -> Optional[str]:
        """
        Parses the completion from the output

        dummy_response: dict[str, Any] = {
            'id': 'chatcmpl-7Sgal7dQAQhcrqrnwsO14w33KBi6h',
            'object': 'chat.completion',
            'created': 1687071263,
            'model': 'gpt-3.5-turbo-0301',
            'usage': {
                'prompt_tokens': 526,
                'completion_tokens': 53,
                'total_tokens': 579
            },
            'choices': [
                {
                    'message': {
                        'role': 'assistant',
                        'content': "SELECT COALESCE(SUM(usage_duration), INTERVAL '0 minutes') AS total_usage_duration\nFROM usage_data\nWHERE user_id = (SELECT user_id FROM user_data WHERE name = 'John')\nAND usage_date >= CURRENT_DATE - INTERVAL '30 days'"
                    },
                    'finish_reason': 'stop',
                    'index': 0
                }
            ]
        }
        """
        choices: Optional[list[dict[str, Any]]] = json.get("choices")
        first_choice: Optional[dict[str, Any]] = choices[0] if choices and len(choices) >= 1 else None
        first_message: Optional[dict[str, Any]] = first_choice.get("message") if first_choice else None
        content: Optional[str] = first_message.get("content") if first_message else None
        return content

    # @lru_cache
    def complete(self, prompt: str) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "system", "content": "You are a helpful assistant."},
                         {"role": "user", "content": prompt}],
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "stop": self.stop
        }
        headers: dict[str, Any] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_KEY}"
        }
        response: requests.Response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response_json: dict[str, Any] = response.json()
        content: Optional[str] = OpenAICompletor.parse_completion(response_json)
        assert content is not None, "content is unexpected None"
        return content

OPENAI_COMPLETOR = OpenAICompletor()

if __name__ == "__main__":
    completor: OpenAICompletor = OpenAICompletor()
    sql_instructions: str = "I'd like to see the total usage duration for user John in the last 30 days."
    sql_prompt: SQLPrompt = SQLPromptFormatter.format(instructions=sql_instructions)
    result = completor.complete(prompt=sql_prompt)