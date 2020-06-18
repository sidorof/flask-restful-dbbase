# create_curl_owner_app_v1.py
import subprocess

filename = "source/owner_app_v1_{:02d}.rst"
all_lines = []
count = 0

def run_cmd(cmd):

    return subprocess.getoutput([cmd.replace(
        'curl', 'curl -s')])

def save(count, cmd):

    spaces = 4
    bash_prefix = '.. code-block:: bash \n'
    json_prefix = '.. code-block:: json \n'
    suffix = '..'

    with open(filename.format(count), 'w') as fobj:
        fobj.write(bash_prefix)
        for line in cmd.split('\n'):
            fobj.write(' ' * spaces + line + '\n')
        fobj.write(suffix)
        fobj.write('\n')

        result = run_cmd(cmd)

        fobj.write('\n')

        fobj.write(json_prefix)
        fobj.write('\n')
        for line in result.split('\n'):
            fobj.write(' ' * spaces + line + '\n')
        fobj.write('\n')
        fobj.write(suffix)
        fobj.write('\n')

    count += 1
    return count

count = save(count, """
# post an order, but no authentication
curl -H "Content-Type: application/json" \\
     http://localhost:5000/orders \\
     -d '{"ownerId": 1, "description": "to do stuff"}'
""")

count = save(count, """
# post an order, but the wrong user
curl -H "Content-Type: application/json" \\
     -H "Authorization: User:2" \\
     http://localhost:5000/orders \\
     -d '{"ownerId": 1, "description": "to do stuff"}'
""")

count = save(count, """
# post an order, with the right user
curl -H "Content-Type: application/json" \\
     -H "Authorization: User:1" \\
     http://localhost:5000/orders \\
     -d '{"ownerId": 1, "description": "to do stuff"}'
""")

count = save(count, """
# get orders, no authorization
curl http://localhost:5000/orders
""")

count = save(count, """
# get orders, with authorization, wrong user
curl -H "Content-Type: application/json" \\
     -H "Authorization: User:2" \\
     http://localhost:5000/orders
""")

count = save(count, """
# get orders, with authorization, right user
curl -H "Content-Type: application/json" \\
     -H "Authorization: User:1" \\
     http://localhost:5000/orders
""")

count = save(count, """
# get meta data for OrderResource
curl -H "Content-Type: application/json" \\
     -H "Authorization: User:1" \\
     http://localhost:5000/meta/orders/single

""")

count = save(count, """
# get meta data for OrderCollectionResource
curl -H "Content-Type: application/json" \\
     -H "Authorization: User:1" \\
     http://localhost:5000/meta/orders/collection

""")

print(count)
