odoo.define('business_appointment.business_appointment_calendarview', function (require) {
"use strict";

    const BusinessAppointmentCalendarController = require('business_appointment.business_appointment_calendarcontroller');
    const BusinessAppointmentCalendarRenderer = require('business_appointment.business_appointment_calendarrenderer');
    const BusinessAppointmentCalendarModel = require('business_appointment.business_appointment_calendarmodel');
    const CalendarView = require('web.CalendarView');
    const viewRegistry = require('web.view_registry');
    const { _lt } = require('web.core');

    const BusinessAppointmentCalendarView = CalendarView.extend({
        config: _.extend({}, CalendarView.prototype.config, {
            Controller: BusinessAppointmentCalendarController,
            Model: BusinessAppointmentCalendarModel,
            Renderer: BusinessAppointmentCalendarRenderer,
        }),
        icon: 'fa-clock-o',
        display_name: _lt('Appointments'),
        viewType: 'appointment_calendar',
    });

    viewRegistry.add('appointment_calendar', BusinessAppointmentCalendarView);

    return BusinessAppointmentCalendarView;

});