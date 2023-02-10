"""
Locust file - Connects to Odoo via jsonrpc
https://locust.io/
https://youtu.be/YoMPeIEqz7U

To see it work, run this file using locust. Make sure the parameters (host, database, port, etc.) are correct.

Findings:
Odoo.sh instance with 1 worker:
    - PartnerUser: 1, GenericUser: 2, CrmUser: 1
    - Max is around 100 simultaneous users with spawn rate of 10. 50+ requests per second.
"""
from locust import task, between
from OdooLocust.OdooLocustUser import OdooLocustUser
from OdooLocust import OdooTaskSet
import random
from mycrmlead import MyCrmLead
from mycrmquotation import MySaleOrder
from OdooLocust import crm


class PartnerUser(OdooLocustUser):
    """
    Locust user for testing CRUD of the Partner model

    Odoo.sh instance with 1 worker:
        - Installed CRM app only
        - Max is around 90 simultaneous users with spawn rate of 5. 35+ requests per second. 2% failure rate. 1 minute

    Odoo on-premise with 4gb memory, 2 CPUs, and 1 worker:
        - Installed CRM app only
        - Max is around 90 simultaneous users with spawn rate of 5. 30+ requests per second. 7% failure rate. 1 minute
    """

    # Set the weight to 1 to enable this locust user
    weight = 0
    wait_time = between(1, 5)

    # Odoo.sh
    database = "cpti-pmreyes-odootest1-main-7119645"
    login = "poch@courtesypoint.com"
    password = "password1"

    # On-premise
    #database = "test"
    #login = "poch@courtesypoint.com"
    #password = "password123"

    # If host is https, protocol = jsonrpcs and port = 443.
    # If host is http, protocol = jsonrpc and port = 8089
    protocol = "jsonrpcs"
    port = 443
    #protocol = "jsonrpc"
    #port = 8069

    # Tasks
    @task(70)
    def read_partners(self):
        partner_model = self.client.get_model('res.partner')
        partner_ids = partner_model.search([])
        partners = partner_model.read(partner_ids, ['name', 'type'])

    @task(15)
    def create_partners(self):
        partner_model = self.client.get_model('res.partner')
        id = partner_model.create({'name': 'locust-new-'+str(random.randint(0, 1000000000)), 'type': 'contact'})
        print('Created Partner with ID = %d' % id)

    @task(10)
    def update_partners(self):
        partner_model = self.client.get_model('res.partner')
        partner_ids = partner_model.search([('name','ilike','locust-new')])

        if len(partner_ids) > 0:
            partner_model.update(partner_ids[0],{'name': 'locust-update-'+str(random.randint(0, 1000000000))})
            print('Updated Partner with ID = %d' % partner_ids[0])

    #@task(5)
    def delete_partners(self):
        partner_model = self.client.get_model('res.partner')
        partner_ids = partner_model.search([('name','ilike','locust-update')])
        if len(partner_ids) > 0:
            partner_model.unlink(partner_ids[0])
            print('Deleted Partner with ID = %d' % partner_ids[0])

    def on_stop(self):
        partner_model = self.client.get_model('res.partner')
        partner_ids = partner_model.search([('name', 'ilike', 'locust-')])
        partner_model.unlink(partner_ids)
        print('Deleted all created Partners')


class GenericUser(OdooLocustUser):
    """
    Locust user for calling the OdooTaskSet.OdooGenericTaskSet tasks

    Odoo.sh instance with 1 worker:
        - Installed CRM app only
        - Max is around 90 simultaneous users with spawn rate of 5. 45+ requests per second. 0% failure rate. 1 minute
    Odoo on-premise with 4gb memory, 2 CPUs, and 1 worker:
        - Installed CRM app only
        - Max is around 90 simultaneous users with spawn rate of 5. 30+ requests per second. 4% failure rate. 1 minute
    """

    # Set the weight to 1 to enable this locust user
    weight = 0
    wait_time = between(1, 5)

    # Odoo.sh
    database = "cpti-pmreyes-odootest1-main-7119645"
    login = "poch@courtesypoint.com"
    password = "password1"

    # On-premise
    # database = "test"
    # login = "poch@courtesypoint.com"
    # password = "password123"

    # If host is https, protocol = jsonrpcs and port = 443.
    # If host is http, protocol = jsonrpc and port = 8089
    protocol = "jsonrpcs"
    port = 443
    # protocol = "jsonrpc"
    # port = 8069

    # Tasks
    tasks = [OdooTaskSet.OdooGenericTaskSet]

class CrmUser(OdooLocustUser):
    """
    Locust user for calling the MyCrmLead tasks

    Odoo.sh instance with 1 worker:
        - Installed CRM and Sales apps
        - Max is around 90 simultaneous users with spawn rate of 5. 25+ requests per second. 22% failure rate. 1 minute
    Odoo on-premise with 4gb memory, 2 CPUs, and 1 worker:
        - Installed CRM app only
        - Max is around 90 simultaneous users with spawn rate of 5. 20+ requests per second. 41% failure rate. 1 minute
    """

    # Set the weight to 1 to enable this locust user
    weight = 1
    wait_time = between(1, 5)

    # Odoo.sh
    database = "cpti-pmreyes-odootest1-main-7119645"
    login = "poch@courtesypoint.com"
    password = "password1"

    # On-premise
    # database = "test"
    # login = "poch@courtesypoint.com"
    # password = "password123"

    # If host is https, protocol = jsonrpcs and port = 443.
    # If host is http, protocol = jsonrpc and port = 8089
    protocol = "jsonrpcs"
    port = 443
    # protocol = "jsonrpc"
    # port = 8069

    # Tasks
    tasks = {MyCrmLead, crm.partner.ResPartner}

# class SalesUser(OdooLocustUser):
#     """
#     Odoo.sh instance with 1 worker:
#         - Max is around 70 simultaneous users with spawn rate of 2. 30+ requests per second.
#     """
#
#     weight = 1
#     wait_time = between(1, 5)
#     database = "cpti-pmreyes-odootest1-main-7028116"
#     login = "poch@courtesypoint.com"
#     password = "42401ebe2a05ae2a22a82718b5e5b07ce261473e"  # API Key
#     protocol = "jsonrpcs"
#     port = 443
#     tasks = {MySaleOrder}

    # General
    # CRUD partners

    # CRM
    # CRUD opportunities
    # CRUD leads

    # Sales
    # CRUD quotations

    # Email Marketing
    # CRUD mailing
    # Send mailing

    # POS

    # Website
    # CRUD blog post
    # Publish blog post
    # CRUD page


    #
