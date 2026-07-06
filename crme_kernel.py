from typing import Dict, Any, Optional


class CRMEKernel:
    """
    Unified CRME Kernel API
    -----------------------
    Single Entry Point for:
    - Session Management
    - Project Management
    - Research Tracking
    """

    def __init__(self, session_engine, project_engine):
        self.session_engine = session_engine
        self.project_engine = project_engine

    # =========================================================
    # 🚀 CREATE NEW RESEARCH SESSION
    # =========================================================

    def start_session(self, project_id: Optional[str] = None, metadata: Dict = None):
        """
        Entry point: start everything from here
        """

        session_id = self.session_engine.create_session(
            project_id=project_id,
            metadata=metadata
        )

        if project_id:
            self.project_engine.handle_session_event(
                "session_created",
                {
                    "session_id": session_id,
                    "project_id": project_id,
                    "metadata": metadata
                }
            )

        return session_id

    # =========================================================
    # 🔁 UPDATE SESSION (LIVE RESEARCH FLOW)
    # =========================================================

    def update(self, session_id: str, update: Dict[str, Any]):
        """
        Main research update pipeline
        """

        # 1. update session
        self.session_engine.update_session(session_id, update)

        # 2. fetch updated session
        session = self.session_engine._load_session(session_id)

        # 3. push to project engine
        self.project_engine.handle_session_event(
            "session_updated",
            {
                "session_id": session_id,
                "state": session["state"]
            }
        )

    # =========================================================
    # 🔗 BIND SESSION TO PROJECT
    # =========================================================

    def bind(self, session_id: str, project_id: str):
        """
        connect session → project explicitly
        """

        self.session_engine.bind_to_project(session_id, project_id)

        snapshot = self.session_engine.get_snapshot(session_id)

        self.project_engine.attach_session(session_id, snapshot)

    # =========================================================
    # 📊 GET LATEST RESEARCH STATE (MAIN API)
    # =========================================================

    def get_latest_state(self, session_id: Optional[str] = None):
        """
        🔥 MOST IMPORTANT FUNCTION
        single call → full CRME state
        """

        # session-level state
        session_snapshot = None
        if session_id:
            session_snapshot = self.session_engine.get_snapshot(session_id)

        # project-level state
        project_state = self.project_engine.export_project()

        return {
            "session": session_snapshot,
            "project": project_state,
            "summary": self._build_summary(session_snapshot, project_state)
        }

    # =========================================================
    # 🧠 RESEARCH SUMMARY ENGINE
    # =========================================================

    def _build_summary(self, session, project):
        """
        lightweight research overview (paper-ready)
        """

        return {
            "total_sessions": len(project.get("sessions", [])),
            "total_decisions": len(project.get("decisions", [])),
            "total_ideas": len(project.get("ideas", [])),
            "last_session_id": session["session_id"] if session else None,
            "project_status": project.get("metadata", {}).get("status", "unknown")
        }

    # =========================================================
    # 📦 EXPORT FOR PAPER / DATASET
    # =========================================================

    def export_research_package(self):
        """
        Q1-ready export bundle
        """

        return {
            "project": self.project_engine.export_project(),
            "sessions": self.session_engine.list_sessions(),
            "timestamp": self._now()
        }

    # =========================================================
    # 🕒 UTIL
    # =========================================================

    def _now(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()

