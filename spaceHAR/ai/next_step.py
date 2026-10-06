def get_next_step(validator):

    status = validator.status()

    current = status.get("current_step")
    next_step = status.get("next_step")

    return {
        "current": current,
        "next": next_step,
        "progress": status.get("progress", 0),
        "finished": status.get("finished", False)
    }