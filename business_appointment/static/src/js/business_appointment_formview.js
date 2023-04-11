odoo.define('business_appointment.business_appointment_formview', function (require) {
"use strict";

    const BusinessAppointmentController = require('business_appointment.business_appointment_formcontroller');
    const FormView = require('web.FormView');
    const viewRegistry = require('web.view_registry');

    const BAOWNFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {Controller: BusinessAppointmentController,}),
    });

    viewRegistry.add('ba_own_form', BAOWNFormView);

    return BAOWNFormView;

});