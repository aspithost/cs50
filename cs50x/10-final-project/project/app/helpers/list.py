def validate_list_keys(list_input, list_keys):
    return type(list_input) == list and len(list_input) and all(item in list_keys for item in list_input)