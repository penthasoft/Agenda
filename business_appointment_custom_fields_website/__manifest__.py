# -*- coding: utf-8 -*-
{
    "name": "Universal Appointments: Custom Fields for Website and Portal",
    "version": "14.0.1.0.1",
    "category": "Website",
    "author": "faOtools",
    "website": "https://faotools.com/apps/14.0/universal-appointments-custom-fields-for-website-and-portal-539",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "business_appointment_custom_fields",
        "business_appointment_website",
        "website_form"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/custom_appointment_contact_info_field.xml",
        "views/custom_business_resource_type_field.xml",
        "views/custom_business_resource_field.xml",
        "views/custom_appointment_product_field.xml",
        "views/templates.xml",
        "data/data.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension to the Universal Appointments app to show custom fields on website",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "0.0",
    "currency": "EUR",
    "post_init_hook": "post_init_hook",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=134&ticket_version=14.0&url_type_id=3",
}