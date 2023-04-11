# -*- coding: utf-8 -*-
{
    "name": "Universal Appointments: Portal and Website",
    "version": "14.0.1.0.5",
    "category": "Website",
    "author": "faOtools",
    "website": "https://faotools.com/apps/14.0/universal-appointments-portal-and-website-535",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "business_appointment",
        "website",
        "auth_signup",
        "rating"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/template.xml",
        "views/res_config_settings.xml",
        "views/business_resource.xml",
        "views/business_resource_type.xml",
        "views/appointment_product.xml",
        "views/business_appointment_core.xml",
        "views/business_appointment.xml",
        "views/full_details_templates.xml",
        "views/templates.xml",
        "views/portal_templates.xml",
        "views/views.xml",
        "reports/appointment_analytic.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension to the Universal Appointments app to schedule appointments on website and in portal",
    "description": """For the full details look at static/description/index.html
* Features * 
- Universal website bookings
- Configurable appointment pages
- Portal control of reservations
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "89.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=130&ticket_version=14.0&url_type_id=3",
}