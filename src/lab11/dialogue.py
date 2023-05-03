from collections import defaultdict
from nomic.gpt4all import GPT4All


class Dialogue:
    def __init__(self):
        self.master_prompts = defaultdict(str)
        self.master_prompts[
            "player"
        ] = "Imagine you are an adventurer embarking on a potentially perilous journey. Speak as an adventurer would, never break character."
        self.gpt4all = GPT4All()
        self.gpt4all.open()

    def get_response(self, speaker: str, prompt: str):
        return self.gpt4all.get_response(self.master_prompts[speaker] + prompt)
