class PromptEngineer:
    def __init__(self, style="digital art"):
        self.base_style = style
        self.scene_number = 0

    def enhance_prompt(self, text_segment):
        self.scene_number += 1
        visual_keywords = self._extract_visual_elements(text_segment)
        enhanced = (
            f"{visual_keywords}, {self.base_style}, "
            "cinematic lighting, high quality, detailed, professional composition"
        )
        enhanced += f", storyboard panel {self.scene_number}"
        return enhanced

    def _extract_visual_elements(self, text):
        visual_mappings = {
            "success": "celebration, upward growth, achievement",
            "challenge": "obstacle, tension, struggle",
            "solution": "innovation, clarity, breakthrough",
            "growth": "ascending, expansion, progress",
            "collaboration": "teamwork, partnership, unity",
            "innovation": "lightbulb, creativity, invention",
            "customer": "happy client, professional meeting",
            "product": "sleek technology, modern device",
            "service": "support, helping hands",
            "problem": "confusion, difficulty, chaos",
            "revenue": "money growth, financial success",
            "sales": "handshake, deal closing",
            "team": "group collaboration",
            "company": "modern office building",
            "market": "competitive landscape",
            "strategy": "planning, chess board",
        }

        txt = text.lower()
        for concept, visual in visual_mappings.items():
            if concept in txt:
                txt = txt.replace(concept, visual)

        words = txt.split()
        stop = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "was", "were", "is", "are", "been",
            "be", "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "must", "can",
        }
        visual_words = [w for w in words if w not in stop and len(w) > 3][:12]
        return " ".join(visual_words) if visual_words else text[:120]