def validate_dict_keys(dictionary, list_keys):
    return type(dictionary) == dict and bool(dictionary) and all(key in list_keys for key in dictionary)


def format_dict(dict_value, list_keys, key_to_add):
    is_true = any(key in dict_value for key in list_keys)
    if is_true:
        dict_value[key_to_add] = {}
    for key in list_keys:
        if key in dict_value:
            if is_true:
                dict_value[key_to_add][key] = dict_value[key]
            del dict_value[key]
    return dict_value


def format_dict_nested_keys(dictionary, list_keys, keys_to_add):
    sub_dict = {}
    for index, key in enumerate(reversed(keys_to_add)):
        sub_dict = {key: sub_dict}
        if index == 0:
            for list_key in list_keys:
                if list_key in dictionary:
                    sub_dict[key][list_key] = dictionary[list_key]
                    del dictionary[list_key]
    first_key = keys_to_add[0]
    if first_key in dictionary and first_key in sub_dict:
        dictionary[first_key].update(sub_dict[first_key])
    else:
        dictionary.update(sub_dict)
    return dictionary


def dict_to_list_values(dictionary, list_keys):
    return [dictionary[key] if key in dictionary else None for key in list_keys]