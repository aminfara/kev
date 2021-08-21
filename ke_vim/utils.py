def check_if_variable(variable_name, value=1):
    return {"name": variable_name, "type": "variable_if", "value": value}


def check_unless_variable(variable_name, value=1):
    return {"name": variable_name, "type": "variable_unless", "value": value}


def set_variable(variable_name, value=1):
    return {"set_variable": {"name": variable_name, "value": value}}


def reset_variable(variable_name):
    return {"set_variable": {"name": variable_name, "value": 0}}


def get_from_key(key_code):
    return {"key_code": key_code}


def get_key_pressed_name(first_key, second_key=""):
    key_code = f"{first_key}_{second_key}" if second_key else first_key
    return f"{key_code}_pressed"


def set_key_pressed(first_key, second_key=""):
    return set_variable(get_key_pressed_name(first_key, second_key))


def reset_key_pressed(first_key, second_key=""):
    return reset_variable(get_key_pressed_name(first_key, second_key))


def if_key_pressed(first_key, second_key=""):
    return check_if_variable(get_key_pressed_name(first_key, second_key))


def unless_key_pressed(first_key, second_key=""):
    return check_unless_variable(get_key_pressed_name(first_key, second_key))


def register_key(first_key, second_key=""):
    # Common structure for both case of having only first_key or having both keys
    manipulator = {
        "type": "basic",
        "from": get_from_key(first_key),
        "to": [
            set_key_pressed(first_key, second_key),
        ],
        "to_delayed_action": {
            "to_if_invoked": [reset_key_pressed(first_key, second_key)]
        },
        "conditions": [
            unless_key_pressed(first_key, second_key),
        ],
    }

    if second_key:
        manipulator["from"] = get_from_key(second_key)
        manipulator["to"].insert(0, reset_key_pressed(first_key))
        manipulator["conditions"].insert(0, if_key_pressed(first_key))

    return manipulator


def execute_key(command_key, action={}, movements=[], first_registered_key="", second_registered_key=""):
    manipulator = {
        "type": "basic",
        "from_key": get_from_key(command_key),
        "to": [],
        "conditions": []
    }

    if first_registered_key:
        manipulator["to"].append(reset_key_pressed(first_registered_key, second_registered_key))
        manipulator["conditions"].append(if_key_pressed(first_registered_key, second_registered_key))

    if movements:
        manipulator["to"].extend(movements)

    if action:
        manipulator["to"].append(action)

    return manipulator

# TODO: merge with get_from_key
def key_code(key, modifiers=None):
    result = {"key_code": key}

    if modifiers:
        result["modifiers"] = modifiers

    return result


def mac_notify(title, message=""):
    return {
        "shell_command": 'osascript -e \'display notification "{message}" with title "\{title}"\''
    }
