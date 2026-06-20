from core.planner import create_plan
from core.executor import run_steps
from core.verifier import verify_result
from core.memory import save_memory


# =========================
# AI DEV OS CORE
# =========================
def dev_os_agent(prompt, user_id="default"):

    # 1. PLANNING
    plan = create_plan(prompt, user_id)

    # 2. EXECUTION
    result = run_steps(plan, user_id)

    # 3. VERIFICATION
    final = verify_result(prompt, result, user_id)

    # 4. MEMORY SAVE
    save_memory(user_id, prompt, final)

    return final
