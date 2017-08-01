# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    Code snippets from openobject-server copyright (C) 2004-2013 OpenERP S.A.
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
from openerp.osv import fields, osv
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
    
class cron(osv.osv):
    _inherit = 'ip.algolia' 
    
    def synchronise_algolia_index(self, cr, uid, context=None):
        aloglia_ids = self.search(cr,uid,[],context=context)
        tmpl_obj =  self.pool.get('product.template')
        objects = []
        if aloglia_ids:
            algolia = self.browse(cr, uid, aloglia_ids[0] , context=context) 
            client = algoliasearch.client.Client(algolia.ip_client_id_algolia, algolia.ip_api_algolia)
            index = client.initIndex(algolia.ip_index_algolia)
            tmpl_ids = tmpl_obj.search(cr,uid,[('ip_aded_to_algolia','=',False),('website_published','=',True),('website_published','=',True)])
            for tmpl in tmpl_obj.browse(cr,uid,tmpl_ids,context=context):
                objects.append(
                               {
                                'id_odoo':tmpl.id,
                                'name_product':tmpl.name,
                                'description_product':tmpl.ip_title,
                                'image_product':tmpl.image_medium,
                                'prix':tmpl.ip_min_price,
                                'ip_url':tmpl.ip_url,
                                'ref_interne':tmpl.ip_ref_interne,
                                }
                               )
            algolia_res = index.addObjects(objects)
            objectID = algolia_res["objectID"]
            tmpl_ids = tmpl_obj.write(cr,uid,tmpl_ids,{'ip_aded_to_algolia':True,'id_algolia':objectID})
        return True