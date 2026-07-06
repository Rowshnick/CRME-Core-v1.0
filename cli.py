import sys
import os

# 🔥 FORCE ROOT CONTEXT (CRITICAL FIX)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from session_engine import SessionEngine
from project_engine import ResearchProject
from crme_repair_tool import CRMERepairTool
from core.session_engine import SessionEngine
from core.project_engine import ResearchProject
from core.crme_kernel import CRMEKernel
from core.crme_repair_tool import CRMERepairTool


# 🚀 FORCE project root as import base
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

BASE_PATH = "/data/data/com.termux/files/home/CRME"

session_engine = SessionEngine(BASE_PATH)
project_engine = ResearchProject("default", BASE_PATH)
crme = CRMEKernel(session_engine, project_engine)
repair_tool = CRMERepairTool(BASE_PATH)


def main():
    if len(sys.argv) < 2:
        print("CRME CLI: start | update | state | check | repair")
        return

    cmd = sys.argv[1]

    if cmd == "start":
        sid = crme.start_session("default")
        print(sid)

    elif cmd == "update":
        sid = sys.argv[2]
        key = sys.argv[3]
        value = sys.argv[4]
        crme.update(sid, {key: [value]})
        print("updated")

    elif cmd == "state":
        sid = sys.argv[2]
        print(crme.get_latest_state(sid))

    elif cmd == "check":
        print(repair_tool.run_health_check())

    elif cmd == "repair":
        print(repair_tool.auto_fix())

    else:
        print("unknown command")


if __name__ == "__main__":
    main()

