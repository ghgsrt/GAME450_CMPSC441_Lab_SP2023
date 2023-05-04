from collections import defaultdict
from TTS.api import TTS
import random
import sounddevice

# from nomic.gpt4all import GPT4All


master_prompts = {
    "player": "Imagine you are an adventurer embarking on a potentially perilous journey. Speak as an adventurer would, never break character.",
    "generic_enemy": "Imagine you are a bandit who hates elves with a deep passion. You live only to rob elves. Never break character.",
}


class Speaker:
    def __init__(self, model_name) -> None:
        if model_name:
            self.voice = TTS(model_name)

        # self.brain = GPT4All()

    # def open(self):
    #     self.brain.open()

    def prompt(self, prompt: str, use_voice=True) -> str:
        # response = self.brain.prompt(prompt)
        response = prompt

        if use_voice:
            if not self.voice:
                random.seed()
                models = TTS.list_models()
                self.voice = TTS(models[random.randint(1, len(models) - 1)])

            wav = self.voice.tts(
                response,
                speaker=self.voice.speakers[0],
                language=self.voice.languages[0],
            )
            sounddevice.play(wav)

        return response


class Dialogue:
    def __init__(self):
        self.journal = []

        self.speakers = {
            "player": Speaker(TTS.list_models()[0]),
            "generic_enemy": Speaker(),
        }

        for speaker in self.speakers:
            # self.speakers[speaker].open()
            self.speakers[speaker].prompt(master_prompts[speaker])

    def prompt(self, speaker: str, prompt: str):
        # response = self.speakers[speaker].prompt(prompt)
        response = prompt
        self.journal.append((speaker, response))
        return response
