# -*- coding: utf-8 -*-

{
    'name': 'Algolia connector',
    'version': '11.0',
    'category': 'algolia_backend',
    'summary': 'Add algolia api credentials and synchronize data',
    'version': '1.0',
    'description': """
        algolia connector engine:
        create algolia account and get the proper credentials from dashboard 
    """,
    'author':  'Ibtissem Zeiri', 
    'depends': ['base','product','website_sale'],
    'data': [
        'views/config.xml',
             ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

