import os
import json
from datetime import datetime


class SessionEngine:
    def __init__(self, base_path):
        self.base_path = base_path
        self.session_dir = os.path.join(base_path, "memory", "sessions")
        os.makedirs(self.session_dir, exist_ok=True)

    # =========================================================
    # CREATE SESSION (FIXED API)
    # =========================================================
    def create_session(self, project_id=None, metadata=None):

        session_id = f"S-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"

        session = {
            "session_id": session_id,
            "project_id": project_id,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "state": {
                "messages": [],
                "decisions": [],
                "goals": [],
                "artifacts": []
            },
            "version": 1
        }

        path = os.path.join(self.session_dir, f"{session_id}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(session, f, indent=2)

        return session_id

    # =========================================================
    # UPDATE SESSION
    # =========================================================
    def update_session(self, session_id, update):

        path = os.path.join(self.session_dir, f"{session_id}.json")

        if not os.path.exists(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            session = json.load(f)

        for k, v in update.items():
            if k in session["state"] and isinstance(session["state"][k], list):
                session["state"][k].extend(v if isinstance(v, list) else [v])
            else:
                session["state"][k] = v

        session["updated_at"] = datetime.utcnow().isoformat()
        session["version"] += 1

        with open(path, "w", encoding="utf-8") as f:
            json.dump(session, f, indent=2)

    # =========================================================
    # SNAPSHOT (FOR KERNEL)
    # =========================================================
    def get_snapshot(self, session_id):

        path = os.path.join(self.session_dir, f"{session_id}.json")

        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            session = json.load(f)

        return session

