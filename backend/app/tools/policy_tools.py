def retrieve_policy_section(policies: dict, message: str):
    msg = message.lower()

    for section in policies.values():
        for keyword in section["keywords"]:
            if keyword in msg:
                return section["content"]

    return None
