import nltk
import re

class TextProcessor:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def segment_narrative(self, text):
        #Break text into logical scenes (3–6)
        sentences = nltk.sent_tokenize(text.strip())
        scenes = [s.strip() for s in sentences if len(s.strip()) > 10]

        # Ensure at least 3 scenes
        if len(scenes) < 3:
            scenes = self._split_long_sentences(scenes)

        return scenes[:6]  # Cap at 6

    def _split_long_sentences(self, scenes):
        expanded = []
        for scene in scenes:
            if len(scene.split()) > 20:
                parts = re.split(r'[;,.]\s+(?=[A-Z])|and |but |so |yet ', scene)
                for p in parts:
                    if len(p.strip()) > 10:
                        expanded.append(p.strip())
            else:
                expanded.append(scene)
        return expanded if expanded else scenes