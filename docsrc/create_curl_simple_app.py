# create_curl_simple_app.py
import subprocess

print("ensure that setup.py install has been run")
input("ensure that example/simple_app is running")

filename = "source/simple_app_{:02d}.rst"
all_lines = []
count = 0
port = {port}

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
# get a book
curl http://localhost:{port}/books/1 \\
    -H "Content-Type: application/json"
""",
)

count = save(
    count,
    f"""
# post a book, but with invalid data
curl http://localhost:{port}/books \\
    -H "Content-Type: application/json" \\
    -d '{"authorId": 1,
         "title": "this is a test woah, this is really a long title, woah, this is really a long title, woah, this is really a long title, woah, this is really a long title, woah, this is really a long title "}'
""",
)

count = save(
    count,
    f"""
# post a book with valid data
curl http://localhost:{port}/books \\
    -H "Content-Type: application/json" \\
    -d '{"authorId": 3,
         "title": "The Algorithm Design Manual",
         "pubYear": 1997,
         "isbn": "0-387-94860-0"}'
""",
)

count = save(
    count,
    f"""
# get all books
curl http://localhost:{port}/books \\
    -H "Content-Type: application/json"
""",
)

count = save(
    count,
    f"""
# get documentation
curl -g http://localhost:{port}/meta/books/single""",
)


print(count)
