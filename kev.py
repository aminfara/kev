import json
from enum import Enum

from ke_vim.utils import (
    check_if_variable,
    key_code,
    mac_notify,
    register_key,
    reset_variable,
    set_variable,
)

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
    manipulator["from"] = key_code(from_key, from_modifiers)
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
    manipulator["from"] = key_code(from_key_second, from_modifiers_second)
    manipulator["conditions"] = [*get_current_vim_mode_conditions(current_vim_mode)]
    manipulator["conditions"].append(check_if_variable(f"{from_key}_pressed", 1))
    manipulator["to"] = [reset_variable(f"{from_key}_pressed")]

    if to_vim_mode:
        manipulator["to"].append(set_variable(to_vim_mode))
        manipulator["to"].append(mac_notify("NORMAL"))
    return manipulator


def get_current_vim_mode_conditions(current_vim_mode):
    conditions = []
    if current_vim_mode == VimMode.NORMAL:
        conditions.append(check_if_variable(VimMode.NORMAL, 1))
        conditions.append(check_if_variable(VimMode.VISUAL, 0))
    elif current_vim_mode == VimMode.VISUAL:
        conditions.append(check_if_variable(VimMode.NORMAL, 0))
        conditions.append(check_if_variable(VimMode.VISUAL, 1))
    else:
        conditions.append(check_if_variable(VimMode.NORMAL, 0))
        conditions.append(check_if_variable(VimMode.VISUAL, 0))
    return conditions


def set_first_key_pressed_variable(pressed_key):
    return {
        "to": [set_variable(f"{pressed_key}_pressed")],
        "to_delayed_action": {
            "to_if_invoked": [
                reset_variable(f"{pressed_key}_pressed"),
                key_code(pressed_key),
            ],
            "to_if_canceled": [
                reset_variable(f"{pressed_key}_pressed"),
                key_code(pressed_key),
            ],
        },
    }


if __name__ == "__main__":
    kev = get_main_body()
    kev["rules"] = get_processed_rules(RULES)
    print(json.dumps(kev, indent=2))
