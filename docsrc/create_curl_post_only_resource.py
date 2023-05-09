# create_curl_post_only_resource.py
import subprocess

print("ensure that setup.py install has been run")
input("ensure that example/post_only_resource is running")

filename = "source/post_only_{:02d}.rst"
all_lines = []
count = 0
port = 5001


def run_cmd(cmd):

    return subprocess.getoutput([cmd.replace("curl", "curl -s ")])


def save(count, cmd):

    spaces = 4
    bash_prefix = ".. code-block:: bash \n"
    json_prefix = ".. code-block:: JSON \n"
    suffix = ".."

    with open(filename.format(count), "w") as fobj:
        fobj.write(bash_prefix)
        for line in cmd.split("\n"):
            fobj.write(" " * spaces + line + "\n")
        fobj.write(suffix)
        fobj.write("\n")

        result = run_cmd(cmd)

        fobj.write("\n")

        fobj.write(json_prefix)
        fobj.write("\n")
        for line in result.split("\n"):
            fobj.write(" " * spaces + line + "\n")
        fobj.write("\n")
        fobj.write(suffix)
        fobj.write("\n")

    count += 1
    return count


count = save(
    count,
    f"""
# create an entry
curl http://localhost:5000/a-model-command \\
    -H "Content-Type: application/json" \\
    -d '{"description": "A test", "num_variable": 42}'
""",
)

count = save(
    count,
    f"""
# create an entry
curl http://localhost:5000/meta/a-model-command/single \\
    -H "Content-Type: application/json"
""",
)


print(count)
