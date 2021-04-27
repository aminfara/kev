def check_if(variable_name, value):
    return {"name": variable_name, "type": "variable_if", "value": value}


def check_unless(variable_name, value):
    return {"name": variable_name, "type": "variable_unless", "value": value}


def set_variable(variable_name, value=1):
    return {"set_variable": {"name": variable_name, "value": value}}


def reset_variable(variable_name):
    return {"set_variable": {"name": variable_name, "value": 0}}


def key_code(key, modifiers=None):
    result = {"key_code": key}

    if modifiers:
        result["modifiers"] = modifiers

    return result


def mac_notify(title, message=""):
    return {
        "shell_command": 'osascript -e \'display notification "{message}" with title "\{title}"\''
    }
