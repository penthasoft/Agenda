# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : ' SITRAD - VF',
    'version' : '1.0',
    'author':'Gobierno Regional de Tacna',
    'category': 'Others',
    'maintainer': 'PenthaSoft Sysm',
    'summary': """Sistema Interoperable de Trámite de Denuncias de Violencia Familiar con aplicación de la Ley Nro. 30364""",
    'description': """

        Proyecto de Operadores Tecnicos GRDIS y Poder Judicial - Corte Suprema de Tacna

    """,
    'website': 'https://www.penthasoft.com/',
    'license': 'LGPL-3',
    'support':'info@penthasoft.com',
    'depends': [ 'base',
        'web',
        'contacts',
        'mail',],
    'data': [
        'views/menu.xml',
        'views/dashboard_views.xml',
        'security/sitrad_system_groups.xml',
        'security/ir.model.access.csv',
        'security/sitrad_system_security.xml',
        'views/sitrad_agresores.xml',
        'views/sitrad_victimas.xml',
        'views/sitrad_denuncias.xml',
        # 'reports/sitrad_apirest_report.xml',
        # 'reports/report_sitrad_apirest.xml',

        'sequence/sitrad_sequence.xml',
    ],
    'qweb': ['static/src/xml/dashboard.xml'],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],

}
