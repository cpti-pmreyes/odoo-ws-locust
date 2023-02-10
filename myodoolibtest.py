"""
Connect to Odoo via jsonrpc using odoo-client-lib
https://github.com/odoo/odoo-client-lib

To see it work, run this file using python. Make sure the parameters (host, database, port, etc.) are correct.
"""
import odoolib

connection = odoolib.get_connection(hostname="cpti-pmreyes-odootest1-main-6995359.dev.odoo.com", database="cpti-pmreyes-odootest1-main-6995359", \
    login="poch@courtesypoint.com", password="password1", protocol="jsonrpcs", port=443)
print("Connecting to...",connection.connector.url)

user_model = connection.get_model("res.users")
ids = user_model.search([("login", "=", "admin")])
user_info = user_model.read(ids[0], ["name"])

print(user_info["name"])
# will print "Administrator"
