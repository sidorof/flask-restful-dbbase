# create_curl_invoice_app.py
from datetime import date
import subprocess
import json

print('ensure that setup.py install has been run')
input('ensure that example/invoice_app.py is running')

filename = "source/invoice_app_{:02d}.rst"
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

invoice = {
    "userId": 1,
    "invoiceDate": date.today().strftime("%F"),
    "invoiceItems": [
        {
            "partCode": "111",
            "units": "1",
            "unitPrice": 20.00
        }, {
            "partCode": "222",
            "units": "5",
            "unitPrice": 15.00
        }
    ]
}

count = save(count, f"""
# post an invoice
curl http://localhost:5000/invoices \\
    -H "Content-Type: application/json" \\
    -d '{json.dumps(invoice, indent=2)}'
""")

count = save(count, """
# get an invoice
curl http://localhost:5000/invoices/1 \\
    -H "Content-Type: application/json"
""")

count = save(count, """
# meta info for POST
curl http://localhost:5000/meta/invoices/single?method=post \\
    -H "Content-Type: application/json"
""")

print(count)
