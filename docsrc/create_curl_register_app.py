# create_curl_post_resource.py
from datetime import date
import subprocess
import json

print('ensure that setup.py install has been run')
input('ensure that example/register_app.py is running')

filename = "source/register_app_{:02d}.rst"
all_lines = []
count = 0

def run_cmd(cmd):

    return subprocess.getoutput([cmd.replace(
        'curl', 'curl -s ')])

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

user = {
    "username": "iam_user",
    "email": "iam_user@example.com",
    "password": "very_secret"
}


count = save(count, f"""
# register
curl http://localhost:5000/register \\
    -H "Content-Type: application/json" \\
    -d '{json.dumps(user, indent=2)}'
""")

token = input('get token')
count = save(count, f"""
# user receives an email with a URL that
# contains the token
curl http://localhost:5000/confirm/{token} \\
    -H "Content-Type: application/json"
""")

count = save(count, """
# Sign-in
curl http:/localhost:5000/sign-in \\
    -H "Content-Type: application/json" \\
    -d '{"username": "iam_user", "password": "very_secret"}'

""")

count = save(count, """
# meta info for register POST
curl http://localhost:5000/meta/register/single?method=post \\
    -H "Content-Type: application/json"
""")

count = save(count, """
# meta info for sign-in POST
curl http://localhost:5000/meta/sign-in/single?method=post \\
    -H "Content-Type: application/json"
""")

print(count)
