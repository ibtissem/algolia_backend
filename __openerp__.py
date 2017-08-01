#-*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-2015 Incontinence Protection
#   (Ali MRISSA) (http://www.incontinence-protection.com/).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Algolia connector',
    'icon': "ip_algolia/static/description/algolia.png",  
    'description': """
Incontinence Protection algolia connector
====================================
    """, 
    'category': 'tools',
    'version' : '8.0.1',
    'author' : 'IP : Ibtissem Zeiri',
    'category' : 'Tools',
    'depends' : ['base','product'],
    'data':[
        'views/algolia.xml', 
        'cron/cron.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
   
}
