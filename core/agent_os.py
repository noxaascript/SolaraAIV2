from core.planner import create_plan
from core.executor import run_steps
from core.verifier import verify_result
from core.memory import add_memory


# =========================
# DEV OS + BROWSER INTELLIGENCE
# =========================
def dev_os_agent(prompt, user_id="default"):

    # 1. planning
    plan = create_plan(prompt)

    # 2. execution
    result = run_steps(plan, user_id)

    # 3. browser-aware verification
    final = verify_result(prompt, result)

    # 4. memory save
    add_memory(user_id, prompt, final)

    return final
