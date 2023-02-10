"""
Connect to Odoo via jsonrpc using urllib.request
https://www.youtube.com/watch?v=J61gRPVSex4&ab_channel=OdooMates

To see it work, run this file using python. Make sure the parameters (host, database, port, etc.) are correct.
"""
import json
import random
import urllib.request

host = "https://cpti-pmreyes-odootest1-main-6995359.dev.odoo.com"
database = "cpti-pmreyes-odootest1-main-6995359"
user = "poch@courtesypoint.com"
password = "password1"
port = 443


def json_rpc(url, method, params):

    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    print("Connecting to...", req.get_full_url())
    print("Request Body...", json.dumps(data).encode())
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})


url = "%s:%d/jsonrpc" % (host,port)
uid = call(url, "common", "login", database, user, password)
print(uid)
