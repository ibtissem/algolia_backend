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
from odoo import models, fields, api, _
from odoo.addons.http_routing.models.ir_http import slug
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
from odoo.exceptions import UserError

class cron(models.Model):
    _inherit = 'website' 
    
#     cron job to synchronise data to index algolia
    @api.multi
    def synchronise_algolia_index(self,api_algolia,client_id_algolia,index_algolia):
        aloglia_ids = self.search([])
        tmpl_obj =  self.env['product.template']
        objects = []
        if aloglia_ids: 
            if client_id_algolia and api_algolia and index_algolia:
                client = algoliasearch.client.Client(api_algolia,client_id_algolia)
                index = client.initIndex(index_algolia)
                tmpl_ids = tmpl_obj.search([('aded_algolia','=',False),('sale_ok','=',True),('website_published','!=',False)])
                for tmpl in tmpl_ids:
                    url = "/shop/product/" + slug(tmpl)
                    object = {
                                    'id_odoo':tmpl.id,
                                    'name_product':tmpl.name, 
                                    'image_product':tmpl.image_small,
                                    'prix':tmpl.list_price, 
                                    'ref_interne':tmpl.default_code,
                                    'url_produit':url,
                                    }
                    algolia_res = index.addObject(object)
                    objectID = algolia_res["objectID"]
                    if objectID:
                        tmpl = tmpl_obj.browse(tmpl.id)
                        tmpl.write({'aded_algolia':True,'id_algolia':objectID})
        return True