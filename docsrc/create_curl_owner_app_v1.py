# create_curl_owner_app_v1.py
import subprocess

print("ensure that setup.py install has been run")
input("ensure that example/owner_app_v1 is running")

filename = "source/owner_app_v1_{:02d}.rst"
all_lines = []
count = 0


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
    """
# post an order, but no authentication
curl http://localhost:5000/orders \\
    -H "Content-Type: application/json" \\
    -d '{"ownerId": 1, "description": "to do stuff"}'
""",
)

count = save(
    count,
    """
# post an order, but the wrong user
curl http://localhost:5000/orders \\
    -H "Content-Type: application/json" \\
    -H "Authorization: User:2" \\
    -d '{"ownerId": 1, "description": "to do stuff"}'
""",
)

count = save(
    count,
    """
# post an order, with the right user
curl http://localhost:5000/orders \\
    -H "Content-Type: application/json" \\
    -H "Authorization: User:1" \\
    -d '{"ownerId": 1, "description": "to do stuff"}'
""",
)

count = save(
    count,
    """
# get orders, no authorization
curl http://localhost:5000/orders
""",
)

count = save(
    count,
    """
# get orders, with authorization, wrong user
curl http://localhost:5000/orders \\
    -H "Content-Type: application/json" \\
    -H "Authorization: User:2"
""",
)

count = save(
    count,
    """
# get orders, with authorization, right user
curl http://localhost:5000/orders \\
    -H "Content-Type: application/json" \\
    -H "Authorization: User:1"
""",
)

count = save(
    count,
    """
# get meta data for OrderResource
curl http://localhost:5000/meta/orders/single \\
    -H "Content-Type: application/json" \\
    -H "Authorization: User:1"
""",
)

count = save(
    count,
    """
# get meta data for OrderCollectionResource
curl http://localhost:5000/meta/orders/collection \\
    -H "Content-Type: application/json" \\
    -H "Authorization: User:1"
""",
)

print(count)
