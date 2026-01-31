# backend/app/agent/memory.py

# In-memory session store (safe for hackathon)
SESSION_STORE = {}


def get_session(session_id: str) -> dict:
    """
    Get existing session or create a new one.
    """

    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = {
            "customer_id": "C0025",  # assumed logged-in user
            "operational": {},
            "human_context": {}
        }

    return SESSION_STORE[session_id]


def update_session(session_id: str, key: str, value):
    """
    Update operational memory safely.
    """

    if session_id not in SESSION_STORE:
        return

    SESSION_STORE[session_id]["operational"][key] = value
