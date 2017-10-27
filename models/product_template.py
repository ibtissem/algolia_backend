# -*- coding: utf-8 -*-
from openerp import models, fields, api, _ 
from odoo.addons.http_routing.models.ir_http import slug
_logger = logging.getLogger(__name__)
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
    
class product_template(models.Model): 
    _inherit = "product.template"   
    
#     mark a product that it was added to algolia index
    aded_algolia = fields.Boolean('Aded to algolia')
#    id algolia to in case of modification of this product we can synchronised to its proper product in algolia index
    id_algolia = fields.Char('Id Produit Algolia')

#    in case of the add of new product add to algolia
    @api.model
    def create(self,values):
            res = super(product_template, self).create(values)
            tmpl = res
            if tmpl:
                try:
                    algolia = self.env['website']
                    aloglia_ids = algolia.search([])
                    tmpl_obj =  self.env['product.template']
                    objects = []
                    if aloglia_ids:
                        url = "/shop/product/" + slug(tmpl)
                        algolia = aloglia_ids[0] 
                        client = algoliasearch.client.Client(algolia.api_algolia,algolia.client_id_algolia)
                        index = client.initIndex(algolia.index_algolia)
                        object =  {
                                    'id_odoo':tmpl.id,
                                    'name_product':tmpl.name, 
                                    'image_product':tmpl.image_small,
                                    'prix':tmpl.list_price, 
                                    'ref_interne':tmpl.default_code,
                                    'url_produit':url,
                                  } 
                        algolia_res = index.add_object(object)
                        objectID = algolia_res["objectID"]
                        if objectID:
                            res.write({'aded_algolia':True,'id_algolia':objectID})
                except:
                    pass
            return res  
         
#     in case of the update of a product updatethe product to algolia
    @api.multi
    def write(self,values):
        res = super(product_template, self).write(values)
        try:
                for tmpl in self:
                    website_obj = self.env['website']
                    website_ids = website_obj.search([])
                    tmpl_obj = self.env['product.template']
                    if website_ids and  self.id_algolia:
                        website = website_ids[0]
                        client = algoliasearch.client.Client(website.api_algolia,website.client_id_algolia)
                        index = client.initIndex(website.index_algolia)
                        object_id = self.id_algolia
                        object_id = int(object_id)
                        url = "/shop/product/" + slug(tmpl)
                        result = index.partial_update_object({
                                            'id_odoo':tmpl.id,
                                            'name_product':tmpl.name, 
                                            'image_product':tmpl.image_small,
                                            'prix':self.list_price, 
                                            'ref_interne':tmpl.default_code,
                                            'url_produit':url,
                                            'objectID': int(tmpl.id_algolia) or 0
                                            })
        except:
                    pass
        return res   
         
#     delete product from algolia if it is deleted from odoo
    def unlink(self):
        for tmpl in self:
            try:
                    website = self.env['website']
                    website_ids = website.search([])
                    tmpl_obj =  self.env['product.template']
                    if website_ids and  tmpl.id_algolia :
                        algolia = website_ids[0]
                        client = algoliasearch.client.Client(algolia.api_algolia,algolia.client_id_algolia)
                        index = client.initIndex(algolia.index_algolia)
                        res = index.delete_object(tmpl.id_algolia)
            except:
                pass
        return super(product_template, self).unlink()