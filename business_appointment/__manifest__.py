# -*- coding: utf-8 -*-
{
    "name": "Universal Appointments and Time Reservations",
    "version": "14.0.1.0.21",
    "category": "Extra Tools",
    "author": "faOtools",
    "website": "https://faotools.com/apps/14.0/universal-appointments-and-time-reservations-534",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "product",
        "resource",
        "calendar",
        "sms",
        "phone_validation",
        "rating"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "reports/business_appointment_report.xml",
        "reports/action_business_appointment_report.xml",
        "data/templates.xml",
        "data/cron.xml",
        "views/views.xml",
        "views/rating_rating.xml",
        "views/business_appointment.xml",
        "views/res_config_settings.xml",
        "views/appointment_product.xml",
        "views/business_resource.xml",
        "views/business_resource_type.xml",
        "views/business_appointment_core.xml",
        "views/business_appointment_custom_search.xml",
        "views/appointment_alarm.xml",
        "views/mail_template.xml",
        "views/sms_template.xml",
        "views/alarm_task.xml",
        "views/res_partner.xml",
        "wizard/make_business_appointment.xml",
        "wizard/choose_appointment_customer.xml",
        "reports/appointment_analytic.xml",
        "views/menu.xml"
    ],
    "qweb": [
        "static/src/xml/*.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool for time-based service management from booking appointment to sale and reviews",
    "description": """For the full details look at static/description/index.html
* Features * 
- Innovative backend scheduling
- &lt;i class=&#39;fa fa-globe&#39;&gt;&lt;/i&gt; Universal website bookings
- Structured service management
- Sale and upsell services
- Flexible configuration: universal appointment application
- Secured appointments
- &lt;i class=&#39;fa fa-gears&#39;&gt;&lt;/i&gt; Custom fields
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "359.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=129&ticket_version=14.0&url_type_id=3",
}