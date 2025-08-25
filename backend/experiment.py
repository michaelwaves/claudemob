from typing import List, Dict, Any
from anthropic import Anthropic
from tqdm import tqdm


class Experiment:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = Anthropic()

    def run_samples(self) -> List[List[Dict[str, str]]]:
        num_samples = self.config.get("num_samples", 1)
        results = []
        
        for _ in tqdm(range(num_samples), desc="Running experiments"):
            result = self._run_conversation()
            results.append(result)
        
        return results

    def _run_conversation(self) -> List[Dict[str, str]]:
        messages = []
        conversation_history = []
        current_message = "Hello! I'm looking forward to our conversation."
        
        for _ in range(self.config["num_turns"]):
            for agent_config in self.config["agents"]:
                response = self.client.messages.create(
                    model=self.config["model_name"],
                    max_tokens=1000,
                    system=agent_config["system_prompt"],
                    messages=conversation_history + [{"role": "user", "content": current_message}]
                )
                
                content = response.content[0].text
                messages.append({
                    "role": "assistant",
                    "speaker": agent_config["name"],
                    "content": content
                })
                
                conversation_history.extend([
                    {"role": "user", "content": current_message},
                    {"role": "assistant", "content": content}
                ])
                
                current_message = content
        
        return messages