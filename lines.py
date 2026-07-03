
file_path: str = './TP_2/Real_1.nc'

lines: list[str] = []
with open(file_path, "r", encoding='utf-8') as file:
    lines = file.readlines()

counter: int = 10
with open(file_path, "w", encoding='utf-8') as file:
    for line in lines:
        line = f"N{counter} {line}"
        file.write(line)
        counter += 10
print('Done')