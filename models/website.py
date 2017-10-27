# -*- coding: utf-8 -*-
from openerp import models, fields, api, _ 
import logging
_logger = logging.getLogger(__name__)
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
    
class algolia(models.Model): 
    _inherit = "website"   
    
    name = fields.Char('Nom')
    api_algolia = fields.Char('Api Key Algolia')
    client_id_algolia = fields.Char('Algolia identifier')
    index_algolia = fields.Char('Algolia Index')

    #Synchronise data every time the api credentials is changed from the configuration page
    @api.multi
    def write(self,vals):
        res = super(algolia,self).write(vals)
        for website in self:
            if vals.get('api_algolia'):
                api_algolia = vals.get('api_algolia') 
            else:
                api_algolia = self.api_algolia
            if vals.get('client_id_algolia'):
                client_id_algolia = vals.get('client_id_algolia') 
            else:
                client_id_algolia = self.client_id_algolia
            if vals.get('index_algolia'):
                index_algolia = vals.get('index_algolia') 
            else:
                index_algolia = self.index_algolia
            if api_algolia and client_id_algolia and index_algolia:
                self.synchronise_algolia_index(api_algolia,client_id_algolia,index_algolia)
        return res
    
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