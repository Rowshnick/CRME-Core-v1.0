import json
import os
from datetime import datetime


class ResearchProject:
    def __init__(
        self,
        project_id,
        title,
        description="",
        paper_target="Q1",
        repository="",
        tags=None
    ):
        self.project_id = project_id
        self.title = title
        self.description = description

        self.paper_target = paper_target
        self.repository = repository

        self.status = "Active"
        self.current_phase = "Initialization"

        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

        self.progress = 0

        self.sessions = []
        self.milestones = []
        self.publications = []

        self.research_ledger = []
        self.decision_log = []
        self.idea_inbox = []
        self.provenance_log = []

        self.tags = tags if tags else []

    # -----------------------------
    # SESSION INTEGRATION (KEY PART)
    # -----------------------------

    def record_session(self, session_data):
        """
        Connect Session Engine → Project Engine
        """
        session_id = session_data.get("session_id")

        if session_id and session_id not in self.sessions:
            self.sessions.append(session_id)

        # Ledger entry
        ledger_entry = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "summary": session_data.get("summary", {}),
            "progress_delta": session_data.get("progress_delta", 0)
        }

        self.research_ledger.append(ledger_entry)

        # Decision tracking
        for d in session_data.get("decisions", []):
            self.decision_log.append({
                "session_id": session_id,
                "decision": d,
                "timestamp": datetime.now().isoformat()
            })

        # Ideas
        for idea in session_data.get("ideas", []):
            self.idea_inbox.append({
                "session_id": session_id,
                "idea": idea,
                "status": "open"
            })

        # Provenance
        for obj in session_data.get("objects", []):
            self.provenance_log.append({
                "object_id": obj,
                "session_id": session_id,
                "project_id": self.project_id
            })

        self._auto_update_progress()
        self.updated_at = datetime.now().isoformat()

    # -----------------------------

    def add_milestone(self, title):
        milestone = {
            "id": f"M-{len(self.milestones)+1:03}",
            "title": title,
            "status": "Pending",
            "completion": 0
        }

        self.milestones.append(milestone)
        self.updated_at = datetime.now().isoformat()

    # -----------------------------

    def _auto_update_progress(self):
        """
        Lightweight heuristic progress model (v1)
        """
        base = len(self.sessions) * 5
        milestone_bonus = sum(m.get("completion", 0) for m in self.milestones) * 0.2

        self.progress = min(100, base + milestone_bonus)

    # -----------------------------

    def set_phase(self, phase):
        self.current_phase = phase
        self.updated_at = datetime.now().isoformat()

    # -----------------------------

    def to_dict(self):
        return self.__dict__

    # -----------------------------

    def save(self, directory="projects"):
        os.makedirs(directory, exist_ok=True)

        path = os.path.join(directory, f"{self.project_id}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

        return path

    # -----------------------------

    @staticmethod
    def load(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        obj = ResearchProject(
            data["project_id"],
            data["title"],
            data.get("description", ""),
            data.get("paper_target", "Q1"),
            data.get("repository", ""),
            data.get("tags", [])
        )

        obj.__dict__.update(data)
        return obj

    # -----------------------------

    def summary(self):
        return {
            "project": self.title,
            "status": self.status,
            "progress": self.progress,
            "sessions": len(self.sessions),
            "milestones": len(self.milestones),
            "ledger_entries": len(self.research_ledger),
            "decisions": len(self.decision_log),
            "ideas": len(self.idea_inbox)
        }

   def handle_session_event(self, event_type, payload):
    """
    🧠 CRME Event Bridge
    اتصال Session → Project
    """

    if event_type == "session_created":
        self.sessions.append(payload.get("session_id"))

    elif event_type == "session_updated":
        self.decisions.extend(payload.get("state", {}).get("decisions", []))

    elif event_type == "goal_added":
        self.ideas.append({
            "type": "goal",
            "data": payload,
            "timestamp": payload.get("timestamp")
        })

    # log provenance
    self.provenance.append({
        "event": event_type,
        "payload": payload,
        "timestamp": payload.get("timestamp")
    })
