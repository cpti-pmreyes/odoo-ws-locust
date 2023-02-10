from OdooLocust.OdooTaskSet import OdooTaskSet
from locust import task

from datetime import date, timedelta

import names
import random

class MyCrmLead(OdooTaskSet):
    list_fields = ["stage_id", "active", "company_id", "calendar_event_count",
                   "quotation_count", "company_id", "user_company_ids", "date_deadline",
                   "create_date", "name", "contact_name", "partner_name", "email_from", "phone", "city", "state_id",
                   "country_id", "partner_id", "user_id", "team_id", "active", "campaign_id",
                   "referred", "medium_id", "probability", "source_id", "message_needaction", "tag_ids", "priority"]
    form_fields = ["stage_id", "active", "company_id", "calendar_event_count", "quotation_count", "sale_amount_total", "sale_order_count",
                   "visitor_page_count", "duplicate_lead_count", "name", "company_currency",
                   "expected_revenue", "recurring_revenue", "recurring_plan", "automated_probability",
                   "is_automated_probability", "probability", "partner_id", "partner_name",
                   "street", "street2", "city", "state_id", "zip", "country_id", "website",
                   "lang_id", "is_blacklisted", "partner_is_blacklisted", "phone_blacklisted",
                   "mobile_blacklisted", "email_state", "phone_state", "partner_email_update", "partner_phone_update",
                   "email_from", "phone", "date_conversion", "user_company_ids", "contact_name",
                   "title", "function", "mobile", "type", "user_id", "date_deadline", "priority", "tag_ids", "team_id",
                   "description", "campaign_id", "medium_id", "source_id", "referred", "date_open",
                   "date_closed", "day_open", "day_close", "display_name"]
    random_id = 11393513

    def _get_search_domain(self):
        name = names.get_first_name()
        return ['|', '|', '|', ('partner_name', 'ilike', name), ('email_from', 'ilike', name), ('contact_name', 'ilike', name), ('name', 'ilike', name)]

    @task(10)
    def test_searchread(self):
        lead_model = self.client.get_model('crm.lead')
        res = lead_model.search_read(
            self._get_search_domain(),
            self.list_fields,
            limit=80,
            context=self.client.get_user_context()
        )
        self.random_id = res[0]['id']

    @task(5)
    def test_websearchread(self):
        lead_model = self.client.get_model('crm.lead')
        res = lead_model.web_search_read(
            self._get_search_domain(),
            self.list_fields,
            limit=80,
            context=self.client.get_user_context()
        )
        self.random_id = res[0]['id']

    @task(20)
    def test_read(self):
        lead_model = self.client.get_model('crm.lead')
        lead_model.read(self.random_id, self.form_fields, context=self.client.get_user_context())

    @task(5)
    def lead_stage_change(self):
        lead_model = self.client.get_model('crm.lead')
        s1 = 229
        s2 = 99
        res1 = lead_model.search([('id', '>', self.random_id), ('stage_id', '=', s1)], limit=1)
        res2 = lead_model.search([('id', '>', self.random_id), ('stage_id', '=', s2)], limit=1)
        if res1:
            lead_model.write(res1[0], {'stage_id': s2}, context=self.client.get_user_context())
        if res2:
            lead_model.write(res2[0], {'stage_id': s1}, context=self.client.get_user_context())

    #@task(5)
    def test_activity(self):
        activity_model = self.client.get_model('mail.activity')
        res = activity_model.create({
            "activity_type_id": 4,
            "calendar_event_id": False,
            "date_deadline": (date(2012, 1 ,1)+timedelta(days=random.randint(1,3650))).isoformat(),
            "note": False,
            "res_id": self.random_id,
            "res_model_id": 276,
            "summary": "Todo",
            "user_id": 294103,
        }, context=self.client.get_user_context())
        activity_model.action_feedback(res, 'Done')

    # @task(5)
    # def test_activity_list(self):
    #     activity_model = self.client.get_model('mail.activity')
    #     activity_model.search_read(
    #         ["&", ["activity_ids", "!=", False], "&", ["activity_user_id", "=", 294103], "|", [ "my_activity_date_deadline", "<", "2022-11-30"], [ "my_activity_date_deadline", "=", "2022-11-30"]],
    #         ["activity_exception_decoration", "activity_exception_icon", "activity_state", "activity_summary", "activity_type_icon", "activity_type_id", "company_id", "user_company_ids", "date_deadline", "create_date", "name", "partner_id", "contact_name", "email_from", "phone", "city", "state_id", "country_id", "user_id", "team_id", "priority", "partner_assigned_id", "date_partner_assign", "activity_ids", "activity_user_id", "my_activity_date_deadline", "activity_calendar_event_id", "campaign_id", "medium_id", "source_id", "company_currency", "expected_revenue", "recurring_revenue_monthly", "recurring_revenue", "recurring_plan", "stage_id", "active", "probability", "tag_ids", "referred", "message_needaction"],
    #         limit=80,
    #     )

    @task
    def test_pipeline_analysis(self):
        lead_model = self.client.get_model('crm.lead')
        lead_model.web_read_group(
            ["&", ["type", "=", "opportunity"], "&", ["create_date", ">=", "2022-01-01 00:00:00"], ["create_date", "<=", "2022-12-31 23:59:59"]],
            ["__count"],
            ["stage_id", "date_deadline:month"],
            context=self.client.get_user_context(),
        )