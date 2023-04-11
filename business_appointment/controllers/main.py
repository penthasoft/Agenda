# -*- coding: utf-8 -*-

import odoo.http as http

from odoo.http import request


class PopUpController(http.Controller):
    """
    Introduced to check popup notifications
    """
    @http.route('/business/appointment/popup/notify', type='json', auth="user")
    def notify(self):
        """
        The method to trigger check of potential popup notifications

        Methods:
         * action_get_next_popup_notif of alarm.task
        """
        res = []
        if request.env.user.has_group('business_appointment.group_ba_user'):
            try:
                res = request.env['alarm.task'].action_get_next_popup_notif()
            except:
                res = []
        return res
