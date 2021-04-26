import json
from enum import Enum
from itertools import chain


DEFAULT_SECOND_KEY_DELAY_MS = 500


class VimMode(str, Enum):
    INSERT = "vim_insert_mode"
    NORMAL = "vim_normal_mode"
    VISUAL = "vim_visual_mode"


RULES = {
    "J,K activate normal mode": [
        ("j", None, "k", None, VimMode.INSERT, VimMode.NORMAL, [])
    ]
}


def get_main_body():
    return {
        "title": "Karabiner-Elements Vim emulation for macOS",
        "homepage": "https://github.com/aminfara/kev",
    }


def get_processed_rules(rules):
    return [
        {"description": k, "manipulators": get_processed_manipulators(v)}
        for k, v in RULES.items()
    ]


def get_processed_manipulators(manipulators):
    results = []
    for manipulator in manipulators:
        results = [*results, *process_manipulator(*manipulator)]

    return results


def process_manipulator(
    from_key,
    from_modifiers,
    from_key_second,
    from_modifiers_second,
    current_vim_mode,
    to_vim_mode,
    to_key_list,
):
    results = []

    manipulator = {"type": "basic"}
    manipulator["from"] = get_from_key(from_key, from_modifiers)
    manipulator["conditions"] = [*get_current_vim_mode_conditions(current_vim_mode)]

    if from_key_second:
        results.append(
            process_second_key_manipulator(
                from_key,
                from_modifiers,
                from_key_second,
                from_modifiers_second,
                current_vim_mode,
                to_vim_mode,
                to_key_list,
            ),
        )
        manipulator = {**manipulator, **set_first_key_pressed_variable(from_key)}
        manipulator["parameters"] = {
            "basic.to_delayed_action_delay_milliseconds": DEFAULT_SECOND_KEY_DELAY_MS
        }

    results.append(manipulator)

    return results


def process_second_key_manipulator(
    from_key,
    from_modifiers,
    from_key_second,
    from_modifiers_second,
    current_vim_mode,
    to_vim_mode,
    to_key_list,
):
    manipulator = {"type": "basic"}
    manipulator["from"] = get_from_key(from_key_second, from_modifiers_second)
    manipulator["conditions"] = [*get_current_vim_mode_conditions(current_vim_mode)]
    manipulator.setdefault("conditions", []).append(
        {"name": f"{from_key}_pressed", "type": "variable_if", "value": 1}
    )
    manipulator["to"] = [{"set_variable": {"name": f"{from_key}_pressed", "value": 0}}]

    if to_vim_mode:
        manipulator["to"].append({"set_variable": {"name": to_vim_mode, "value": 1}})
        manipulator["to"].append(
            {"shell_command": 'osascript -e \'display notification with title "NORMAL"'}
        )
    return manipulator


def get_from_key(from_key, from_modifiers):
    result = {"key_code": from_key}

    if from_modifiers:
        result["modifiers"] = from_modifiers

    return result


def get_current_vim_mode_conditions(current_vim_mode):
    conditions = []
    if current_vim_mode == VimMode.NORMAL:
        conditions.append(get_condition_variable_if(VimMode.NORMAL, 1))
        conditions.append(get_condition_variable_if(VimMode.VISUAL, 0))
    elif current_vim_mode == VimMode.VISUAL:
        conditions.append(get_condition_variable_if(VimMode.NORMAL, 0))
        conditions.append(get_condition_variable_if(VimMode.VISUAL, 1))
    else:
        conditions.append(get_condition_variable_if(VimMode.NORMAL, 0))
        conditions.append(get_condition_variable_if(VimMode.VISUAL, 0))
    return conditions


def get_condition_variable_if(variable_name, value):
    return {"name": variable_name, "type": "variable_if", "value": value}


def set_first_key_pressed_variable(key_code):
    return {
        "to": [{"set_variable": {"name": f"{key_code}_pressed", "value": 1}}],
        "to_delayed_action": {
            "to_if_invoked": [
                {"set_variable": {"name": f"{key_code}_pressed", "value": 0}},
                {"key_code": key_code},
            ],
            "to_if_canceled": [
                {"set_variable": {"name": f"{key_code}_pressed", "value": 0}},
                {"key_code": key_code},
            ],
        },
    }


if __name__ == "__main__":
    kev = get_main_body()
    kev["rules"] = get_processed_rules(RULES)
    print(json.dumps(kev, indent=2))
