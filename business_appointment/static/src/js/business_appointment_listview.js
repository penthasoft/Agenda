odoo.define('business_appointment.business_appointment_listview', function (require) {
"use strict";

    const BusinessAppointmentListController = require('business_appointment.business_appointment_list_controller');
    const ListView = require('web.ListView');
    const viewRegistry = require('web.view_registry');

    const BAOWNListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {Controller: BusinessAppointmentListController,}),
    });

    viewRegistry.add('ba_own_list', BAOWNListView);

    return BAOWNListView;

});