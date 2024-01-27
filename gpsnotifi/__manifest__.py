# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'GPS Notificador',
    'version' : '1.0',
    'author':'PenthaSoft Sysm',
    'category': 'Sales',
    'maintainer': 'PenthaSoft Sysm',
    'summary': """Base de datos de notificaciones y geolocalizacion de entrega""",
    'description': """

        Facturacion de Convenios para CR Fleming Santiago - Arica  / Chile

    """,
    'website': 'https://erp.crfleming.cl/',
    'license': 'LGPL-3',
    'support':'info@crfleming.cl',
    'depends': [ 'base', 'contacts', 'mail'],
    'data': [
        'security/gpsnotifi_system_groups.xml',
        'security/ir.model.access.csv',
        'security/gpsnotifi_system_security.xml',
        'views/menu.xml',
        'views/gpsnotifi_apirest.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],

}
