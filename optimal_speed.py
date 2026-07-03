import sys
from math import sqrt
from dataclasses import dataclass


# Parámetros de máquina (simulados)
RAPID_SPEED = 3000  # mm/min - velocidad de posicionamiento rápido (G00)
LINEAR_CUT_SPEED = 2000  # mm/min - velocidad de corte lineal (G01)
CIRCULAR_CUT_SPEED = 900  # mm/min - velocidad de corte circular (G02/G03)
TOOL_DIAMETER = 3.175  # mm
MAX_ACCEL = 1200.00  # mm/s2
MAX_FEED = 2000
MAX_SPINDLE_RPM = 10000
MATERIAL_FACTOR = 1.0  # factor de ajuste por material


@dataclass()
class Codes:
    MOVEMENT_LINE = 0
    DRAW_LINE = 1
    L_R_CIRCLE = 2
    R_L_CIRCLE = 3
    CONFIG_CODES = [
        "g54",
        "g55",
        "g56",
        "g57",
        "g90.1",
        "g90",
        "g91",
        "g17",
        "g20",
        "g21",
    ]


@dataclass()
class ActionTypes:
    CUT = "g"
    ESPECIAL = "m"
    LINE_NUMBER = "n"
    FEED_SPEED = "f"
    COMMENT_SYMBOLS = "(#"


def calc_rapid_speed() -> float:
    return RAPID_SPEED


def calc_linear_speed() -> float:
    return LINEAR_CUT_SPEED * MATERIAL_FACTOR


def calc_circular_speed(radius: float) -> float:
    if radius <= 0:
        return LINEAR_CUT_SPEED
    v_max_mm_s = sqrt(MAX_ACCEL * radius)
    v_max_mm_min = v_max_mm_s * 60
    return min(v_max_mm_min, LINEAR_CUT_SPEED) * MATERIAL_FACTOR


def calc_optimal_speed(active_mode: int, radius: float = 0) -> float:
    match active_mode:
        case Codes.MOVEMENT_LINE:
            return calc_rapid_speed()
        case Codes.DRAW_LINE:
            return calc_linear_speed()
        case Codes.L_R_CIRCLE | Codes.R_L_CIRCLE:
            return calc_circular_speed(radius)
        case _:
            return calc_linear_speed()


def is_comment_line(raw_line: str) -> bool:
    stripped = raw_line.strip()
    for ch in ActionTypes.COMMENT_SYMBOLS:
        if ch in stripped:
            return True
    return False


def parse_arg_format(element: str) -> str:
    if "x" in element or "y" in element or "z" in element:
        return element.lower()
    else:
        return element.upper()


def main() -> None:
    file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    if not output_file_path:
        output_file_path = "./result.nc"
    active_mode: int = Codes.MOVEMENT_LINE
    output_file = open(output_file_path, "w", encoding="utf-8")
    with open(file_path, "r+", encoding="utf-8") as raw_code_file:
        raw_lines = raw_code_file.readlines()

        for index, line in enumerate(raw_lines, 1):
            print(f"\n {index * 10}", end=" ")
            print(repr(line))

            raw_line = line.rstrip("\n\r")

            if is_comment_line(raw_line):
                output_file.write(raw_line + "\n")
                continue

            lowered = line.lower()
            components: list[str] = lowered.split()

            if "z" in lowered:
                active_mode = Codes.MOVEMENT_LINE
                args = list(map(parse_arg_format, raw_line.split()))
                output_file.write(" ".join(args) + "\n")
                continue

            total_elements = len(components)
            if total_elements <= 2 and (
                ActionTypes.LINE_NUMBER in components[0]
                or ActionTypes.ESPECIAL in components[0]
            ):
                print("line contains only number or especial character")
                output_file.write(raw_line.upper() + "\n")
                continue

            action = components[1]
            action_type = action[0]
            action_code: int = 0

            if action_type == ActionTypes.CUT:
                action_code = int(float(action[1:]))
                active_mode = action_code

            if f"{action_type}{action_code}" in Codes.CONFIG_CODES:
                print("is config line")
                output_file.write(raw_line.upper() + "\n")
                continue

            if active_mode == Codes.MOVEMENT_LINE:
                args = list(map(parse_arg_format, raw_line.split(" ")))
                output_file.write(" ".join(args) + "\n")
                continue

            action_args: list[str] = []
            if action_type != ActionTypes.CUT and action_type != ActionTypes.ESPECIAL:
                action_args = components[1:]
            else:
                action_args = components[2:]

            if action_args and ActionTypes.FEED_SPEED in action_args[-1]:
                action_args.pop(-1)

            radius = 0.0
            if active_mode == Codes.L_R_CIRCLE or active_mode == Codes.R_L_CIRCLE:
                if len(action_args) >= 3:
                    i: float = 0
                    j: float = 0
                    for arg in action_args:
                        if arg.startswith("r"):
                            radius = float(arg[1:])
                        elif arg.startswith("i"):
                            i = float(arg[1:])
                        elif arg.startswith("j"):
                            j = float(arg[1:]) if len(action_args) > 3 else 0

                    if not radius and i and j:
                        radius = (i**2 + j**2) ** 0.5

            optimal_speed = calc_optimal_speed(active_mode, radius)
            print(
                f"  {action_code=} | {active_mode=} | {action_args=} | Vopt={optimal_speed:.1f} mm/min"
            )

            action_args = list(map(parse_arg_format, action_args))

            line_number: int = index * 10
            result_line: str = f"N{line_number} G0{active_mode} {' '.join(action_args)} F{optimal_speed:.2f}\n"
            print(result_line)
            output_file.write(result_line)

    output_file.close()


if __name__ == "__main__":
    main()
