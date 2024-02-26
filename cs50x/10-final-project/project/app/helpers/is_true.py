def is_true(val):
    return type(val) == str and val.strip().lower() == "true"