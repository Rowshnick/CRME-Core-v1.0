class MemoryEngine:
    def __init__(self, text):
        self.text = text

    def extract(self):
        goals = []
        decisions = []
        steps = []

        for line in self.text.split("\n"):
            l = line.lower()

            if "goal" in l or "هدف" in l:
                goals.append(line)

            if "decision" in l or "تصمیم" in l:
                decisions.append(line)

            if "next" in l or "بعد" in l:
                steps.append(line)

        return {
            "goals": goals,
            "decisions": decisions,
            "next_steps": steps
        }
