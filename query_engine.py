import json
import os

from core.semantic_engine import SemanticEngine
from core.memory_intelligence import MemoryIntelligence

# 🧠 v0.9 NEW LAYERS
from core.agent_brain import AgentBrain
from core.auto_memory import AutoMemory


class QueryEngine:
    def __init__(self, base_path):
        self.base_path = base_path
        self.index_path = os.path.join(base_path, "memory", "index.json")

        # -------------------------
        # Load index
        # -------------------------
        with open(self.index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

        # -------------------------
        # Semantic layer
        # -------------------------
        self.semantic = SemanticEngine(self.index)

        # -------------------------
        # Intelligence layer (v0.8+)
        # -------------------------
        self.intelligence = MemoryIntelligence(self.index)

        # -------------------------
        # 🧠 v0.9 Agent layers
        # -------------------------
        self.brain = AgentBrain(self.index)
        self.auto = AutoMemory(self.index, self.brain)

        # apply scoring
        self.index = self.intelligence.apply_scoring()

    # =========================================================
    # BASIC SEARCH
    # =========================================================
    def search_by_type(self, obj_type):
        return [
            o for o in self.index.get("objects", [])
            if o.get("type") == obj_type
        ]

    def search_by_keyword(self, keyword):
        keyword = keyword.lower()
        return [
            o for o in self.index.get("objects", [])
            if keyword in o.get("content", "").lower()
        ]

    # =========================================================
    # GRAPH TRACE
    # =========================================================
    def trace_from_object(self, object_id):
        chain = [object_id]
        current = object_id

        relations = self.index.get("relations", [])

        while True:
            next_rel = next(
                (r for r in relations if r["from"] == current),
                None
            )

            if not next_rel:
                break

            chain.append(next_rel["to"])
            current = next_rel["to"]

        return chain

    # =========================================================
    # SESSION
    # =========================================================
    def get_latest_session(self):
        sessions = self.index.get("sessions", [])
        return sessions[-1] if sessions else {"status": "no_session"}

    def load_session_summary(self):
        path = os.path.join(self.base_path, "memory", "session_summary.json")

        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # =========================================================
    # SEMANTIC
    # =========================================================
    def semantic_search(self, text, threshold=0.2):
        return self.semantic.find_similar(text, threshold)

    # =========================================================
    # CLUSTERING
    # =========================================================
    def cluster(self):
        return self.semantic.cluster_by_type()

    # =========================================================
    # 🧠 v0.9 AUTONOMOUS MEMORY HOOK
    # =========================================================
    def auto_ingest(self, text):
        """
        Autonomous memory decision layer
        """
        result = self.auto.process(text)

        if not result:
            return {"stored": False, "reason": "not important"}

        # convert decision → object-like structure
        return {
            "stored": True,
            "object": result
        }

    # =========================================================
    # 🧠 SMART QUERY (Agent-aware)
    # =========================================================
    def smart_query(self, text):
        text_l = text.lower()

        # -------------------------
        # CONTINUE SESSION
        # -------------------------
        if "continue" in text_l:
            summary = self.load_session_summary()
            return {
                "status": "resumed",
                "summary": summary
            }

        # -------------------------
        # AUTO MEMORY MODE (NEW v0.9)
        # -------------------------
        if "auto" in text_l or "ingest" in text_l:
            return self.auto_ingest(text)

        # -------------------------
        # STRUCTURED QUERIES
        # -------------------------
        if "decision" in text_l:
            return self.search_by_type("Decision")

        if "goal" in text_l:
            return self.search_by_type("Goal")

        if "task" in text_l:
            return self.search_by_type("Task")

        if "session" in text_l:
            return self.get_latest_session()

        if "cluster" in text_l:
            return self.cluster()

        if "trace" in text_l:
            objs = self.index.get("objects", [])
            if objs:
                return self.trace_from_object(objs[-1]["id"])
            return []

        # -------------------------
        # INTELLIGENCE LAYER
        # -------------------------
        if "insight" in text_l or "summary" in text_l:
            return self.intelligence.summarize()

        # -------------------------
        # SEMANTIC FALLBACK
        # -------------------------
        return self.semantic_search(text)

    # =========================================================
    # PUBLIC API
    # =========================================================
    def query(self, text):
        return self.smart_query(text)

    def search(self, text):
        return self.smart_query(text)

