import json
from enum import Enum

from ke_vim.rules import (
    activate_insert_mode_rule,
    activate_normal_mode_rule,
    normal_mode_movement_rule,
)


def get_main_body():
    return {
        "title": "Karabiner-Elements Vim emulation for macOS",
        "homepage": "https://github.com/aminfara/kev",
    }


if __name__ == "__main__":
    kev = get_main_body()
    kev["rules"] = [
        activate_normal_mode_rule(),
        activate_insert_mode_rule(),
        normal_mode_movement_rule(),
    ]
    print(json.dumps(kev, indent=2))
