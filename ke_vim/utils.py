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


def if_vim_insert():
    return [
        check_unless_variable("vim_normal_mode"),
        check_unless_variable("vim_visual_mode"),
    ]


def if_vim_normal():
    return [
        check_if_variable("vim_normal_mode"),
        check_unless_variable("vim_visual_mode"),
    ]


def if_vim_visual():
    return [
        check_if_variable("vim_visual_mode"),
        check_unless_variable("vim_normal_mode"),
    ]


def set_vim_insert():
    return [reset_variable("vim_normal_mode"), reset_variable("vim_visual_mode")]


def set_vim_normal():
    return [set_variable("vim_normal_mode"), reset_variable("vim_visual_mode")]


def set_vim_visual():
    return [reset_variable("vim_normal_mode"), set_variable("vim_visual_mode")]


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


def execute_key(
    command_key,
    actions=[],
    first_registered_key="",
    second_registered_key="",
):
    manipulator = {
        "type": "basic",
        "from": get_from_key(command_key),
        "to": [],
        "conditions": [],
    }

    if first_registered_key:
        manipulator["to"].append(
            reset_key_pressed(first_registered_key, second_registered_key)
        )
        manipulator["conditions"].append(
            if_key_pressed(first_registered_key, second_registered_key)
        )

    if actions:
        manipulator["to"].extend(actions)

    return manipulator


# TODO: merge with get_from_key
def key_code(key, modifiers=None):
    result = {"key_code": key}

    if modifiers:
        result["modifiers"] = modifiers

    return result


def mac_notify(title, message=""):
    return [
        {
            "shell_command": 'osascript -e \'display notification "{message}" with title "\{title}"\''
        }
    ]


def move_left():
    return [{"key_code": "left_arrow"}]


def select_left():
    moves = move_left()
    moves[0]["modifiers"] = ["left_shift"]
    return moves


def move_right():
    return [{"key_code": "right_arrow"}]


def select_right():
    moves = move_right()
    moves[0]["modifiers"] = ["left_shift"]
    return moves


def move_up():
    return [{"key_code": "up_arrow"}]


def select_up():
    moves = move_up()
    moves[0]["modifiers"] = ["left_shift"]
    return moves


def move_down():
    return [{"key_code": "down_arrow"}]


def select_down():
    moves = move_down()
    moves[0]["modifiers"] = ["left_shift"]
    return moves


def move_line():
    return [
        {"key_code": "left_arrow", "modifiers": ["left_command"]},
        {"key_code": "left_arrow", "modifiers": ["left_command"]},
        {"key_code": "right_arrow", "modifiers": ["left_command"]},
    ]


def select_line():
    moves = move_line()
    moves[2]["modifiers"].append("left_shift")
    return moves


def move_word_begining():
    return [{"key_code": "left_arrow", "modifiers": ["left_alt"]}]


def select_word_begining():
    moves = move_word_begining()
    moves[0]["modifiers"].append("left_shift")
    return moves


def move_word_end():
    return [{"key_code": "right_arrow", "modifiers": ["left_alt"]}]


def select_word_end():
    moves = move_word_end()
    moves[0]["modifiers"].append("left_shift")
    return moves


def move_line_very_begining():
    return [
        {"key_code": "left_arrow", "modifiers": ["left_command"]},
        {"key_code": "left_arrow", "modifiers": ["left_command"]},
    ]


def select_line_very_begining():
    moves = move_line_very_begining()
    moves[0]["modifiers"].append("left_shift")
    moves[1]["modifiers"].append("left_shift")
    return moves


def move_line_begining():
    return [
        {"key_code": "left_arrow", "modifiers": ["left_command"]},
    ]


def select_line_begining():
    moves = move_line_begining()
    moves[0]["modifiers"].append("left_shift")
    return moves


def move_line_end():
    return [
        {"key_code": "right_arrow", "modifiers": ["left_command"]},
    ]


def select_line_end():
    moves = move_line_end()
    moves[0]["modifiers"].append("left_shift")
    return moves


def move_page_begining():
    return [{"key_code": "up_arrow", "modifiers": ["left_command"]}]


def select_page_begining():
    moves = move_page_begining()
    moves[0]["modifiers"].append("left_shift")
    return moves


def move_page_end():
    return [{"key_code": "down_arrow", "modifiers": ["left_command"]}]


def select_page_end():
    moves = move_page_end()
    moves[0]["modifiers"].append("left_shift")
    return moves


def move_paragraph_begining():
    return [{"key_code": "a", "modifiers": ["left_control"]}]


def select_paragraph_begining():
    moves = move_paragraph_begining()
    moves[0]["modifiers"].append("left_shift")
    return moves


def move_paragraph_end():
    return [{"key_code": "e", "modifiers": ["left_control"]}]


def select_paragraph_end():
    moves = move_paragraph_end()
    moves[0]["modifiers"].append("left_shift")
    return moves


def get_cut():
    return [{"key_code": "x", "modifiers": ["left_command"]}]


def get_copy():
    return [{"key_code": "c", "modifiers": ["left_command"]}]


def get_paste():
    return [{"key_code": "v", "modifiers": ["left_command"]}]


def get_delete():
    return [{"key_code": "delete_or_backspace"}]


def prepend_conditions(manipulator, conditions):
    manipulator["conditions"] = conditions + manipulator["conditions"]


def fast_delay_action():
    return {"parameters": {"basic.to_delayed_action_delay_milliseconds": 100}}
