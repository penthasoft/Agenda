# -*- coding: utf-8 -*

from odoo.addons.bus.controllers.main import BusController
from odoo.http import request


class BABusController(BusController):
    """
    Overwrite to add alarm.task prosessing
    """
    def _poll(self, dbname, channels, last, options):
        """
        Re-write to process alarm.task
        """
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'alarm.task', request.env.user.partner_id.id))
        return super(BABusController, self)._poll(dbname, channels, last, options)
