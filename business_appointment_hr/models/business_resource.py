#coding: utf-8

from odoo import _, api, fields, models


class business_resource(models.Model):
    """
    Overwrite to link business resources with employee
    """
    _inherit = "business.resource"

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        """
        Onchange method for employee_id
        """
        for resource in self:
            if resource.employee_id:
                resource.name = resource.employee_id.name
                if resource.employee_id.user_id:
                    resource.user_id = resource.employee_id.user_id
                if resource.employee_id.resource_calendar_id:
                    resource.resource_calendar_id = resource.employee_id.resource_calendar_id

    employee_id = fields.Many2one("hr.employee", string="Employee", ondelete="cascade",)

    _sql_constraints = [('employee_id_uniq', 'unique(employee_id)', _('Resource per each employee should be unique!'))]

    @api.model
    def create(self, vals):
        """
        Overwrite to retrieve resource from employee
        """
        if vals.get("employee_id"):
            resource_id = self.env["hr.employee"].browse(vals.get("employee_id")).resource_id
            vals.update({"resource_id": resource_id.id})
            if not vals.get("tz"):
                vals.update({"tz": resource_id.tz})
        return super(business_resource, self).create(vals)

    def write(self, vals):
        """
        Overwrite to retrieve resource from employee
         1. When employee is chosen --> make previous resource deleted (if not employee). Take one from employee
         2. When employee becomes empty --> create a new resource
        """
        res = False
        for resource in self:
            resource_vals = vals.copy()
            if resource_vals.get("employee_id"):
                # 1
                resource_id = self.env["hr.employee"].browse(resource_vals.get("employee_id")).resource_id.id
                resource_vals.update({"resource_id": resource_id})
                if not resource.employee_id:
                    resource.resource_id.active = False
            elif resource_vals.get("employee_id") is not None:
                # 2
                resource_id = resource.resource_id.copy({'name': resource.name})
                resource_vals.update({"resource_id": resource_id.id})
            res = super(business_resource, resource).write(resource_vals)
        return res
