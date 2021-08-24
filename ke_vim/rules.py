from ke_vim.utils import (
    execute_key,
    fast_delay_action,
    key_code,
    if_vim_insert,
    if_vim_normal,
    mac_notify,
    move_down,
    move_left,
    move_right,
    move_up,
    prepend_conditions,
    register_key,
    reset_key_pressed,
    set_vim_insert,
    set_vim_normal,
)


def insert_mode_j_manipulator():
    j_manipulator = register_key("j")
    prepend_conditions(j_manipulator, if_vim_insert())
    j_manipulator["to_delayed_action"]["to_if_invoked"] = [
        reset_key_pressed("j"),
        key_code("j"),
    ]
    j_manipulator["to_delayed_action"]["to_if_canceled"] = [
        reset_key_pressed("j"),
        key_code("j"),
    ]
    return j_manipulator


def insert_mode_k_manipulator():
    k_manipulator = execute_key("k", first_registered_key="j")
    prepend_conditions(k_manipulator, if_vim_insert())
    k_manipulator["to_delayed_action"] = {
        "to_if_invoked": [key_code("delete_or_backspace")] + set_vim_normal()
    }
    k_manipulator = {**k_manipulator, **fast_delay_action()}

    return k_manipulator


def normal_mode_h_manipulator():
    h_manipulator = execute_key("h", actions=move_left())
    prepend_conditions(h_manipulator, if_vim_normal())
    return h_manipulator


def normal_mode_j_manipulator():
    j_manipulator = execute_key("j", actions=move_down())
    prepend_conditions(j_manipulator, if_vim_normal())
    return j_manipulator


def normal_mode_k_manipulator():
    k_manipulator = execute_key("k", actions=move_up())
    prepend_conditions(k_manipulator, if_vim_normal())
    return k_manipulator


def normal_mode_l_manipulator():
    l_manipulator = execute_key("l", actions=move_right())
    prepend_conditions(l_manipulator, if_vim_normal())
    return l_manipulator


def normal_mode_i_manipulator():
    i_manipulator = execute_key("i", actions=set_vim_insert())
    prepend_conditions(i_manipulator, if_vim_normal())
    return i_manipulator


def activate_normal_mode_rule():
    return {
        "description": "(kev 1) Activate normal mode with j,k",
        "manipulators": [insert_mode_k_manipulator(), insert_mode_j_manipulator()],
    }


def activate_insert_mode_rule():
    return {
        "description": "(kev 2) Activate insert mode with i",
        "manipulators": [normal_mode_i_manipulator()],
    }


def normal_mode_movement_rule():
    return {
        "description": "(kev 3) Move in normal mode h,j,k,l",
        "manipulators": [
            normal_mode_h_manipulator(),
            normal_mode_j_manipulator(),
            normal_mode_k_manipulator(),
            normal_mode_l_manipulator(),
        ],
    }
