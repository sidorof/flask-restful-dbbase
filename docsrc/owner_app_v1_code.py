# owner_app_v1_code.py
import subprocess

source_file = "../examples/owner_app_v1.py"

filename = "source/owner_app_v1_code_{:02d}.rst"
all_lines = []
count = 0

with open(source_file) as fobj:
    source_lines = fobj.readlines()


def save(count, text):

    prefix = ".. code-block:: python \n"
    suffix = ".."

    with open(filename.format(count), "w") as fobj:
        fobj.write(prefix)
        fobj.write("\n")

        fobj.writelines(text)
        fobj.write(suffix)

    count += 1
    return count


def find_block(start, end):

    spaces = 4
    temp = []
    append = False
    for line in source_lines:
        if end is not None and line.strip() == end:
            return "".join(temp)
        if append:
            temp.append(" " * spaces + line)
        if line.strip() == start:
            append = True

    return "".join(temp)


locations = [
    ["# initialize", "# define users"],
    ["# define users", "# define orders"],
    ["# define orders", "# end database setup"],
    ["# end database setup", "# mock authentication"],
    ["# mock authentication", "# create owner resources"],
    ["# create owner resources", "# order resources"],
    ["# order resources", "# add the resources to the API"],
    ["# add the resources to the API", None],
]

for start, end in locations:
    text = find_block(start, end)
    count = save(count, text)
