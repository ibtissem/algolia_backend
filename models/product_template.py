# -*- coding: utf-8 -*-
from openerp import models, fields, api, _ 
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
    
class product_template(models.Model): 
    _inherit = "product.template"   
    
    aded_algolia = fields.Boolean('Aded to algolia')
    algolia = fields.Char('Id Produit Algolia')

#     def create(self,values):
#             res = super(product_template, self).create(values)
#             tmpl = res
#             if tmpl:
#                 try:
#                     algolia = self.pool.get('algolia.config')
#                     aloglia_ids = algolia.search(cr,uid,[],context=context)
#                     tmpl_obj =  self.pool.get('product.template')
#                     objects = []
#                     if aloglia_ids:
#                         algolia = algolia.browse(cr, uid, aloglia_ids[0] , context=context) 
#                         client = algoliasearch.client.Client(algolia.client_id_algolia, algolia.api_algolia)
#                         index = client.initIndex(algolia.index_algolia)
#                         object =  {
#                                             'id_odoo':tmpl.id,
#                                             'name_product':tmpl.name, 
#                                             'image_product':tmpl.image_small,
#                                             'prix':tmpl.list_price, 
#                                             'ref_interne':tmpl.default_code,
#                                             } 
#                         algolia_res = index.addObject(object)
#                         objectID = algolia_res["objectID"]
#                         if objectID:
#                             self.write(cr,uid,res,{'aded_algolia':True,'id_algolia':objectID})
#                 except:
#                     pass
#             return res   
# 
#     def write(self, cr, uid, ids, values, context=None):
#         res = super(product_template, self).write(cr,uid,ids,values,context=context)
#         if ids:
#             if isinstance(ids, (int, long)):
#               ids = [ids]
#             
#             tmpl = self.browse(cr,uid,ids[0],context=context) 
#             if tmpl:
#                 try:
#                     algolia = self.pool.get('algolia.config')
#                     aloglia_ids = algolia.search(cr,uid,[],context=context)
#                     tmpl_obj =  self.pool.get('product.template')
#                     if aloglia_ids and  tmpl.id_algolia:
#                         algolia = algolia.browse(cr, uid, aloglia_ids[0] , context=context) 
#                         client = algoliasearch.client.Client(algolia.client_id_algolia, algolia.api_algolia)
#                         index = client.initIndex(algolia.index_algolia)
#                         index.partial_update_object({
#                                             'id_odoo':tmpl.id,
#                                             'name_product':tmpl.name, 
#                                             'image_product':tmpl.image_small,
#                                             'prix':tmpl.list_price, 
#                                             'ref_interne':tmpl.default_code,
#                                             'objectID':tmpl.id_algolia or 0
#                                             })
#                 except:
#                     pass
#         return res   
#         
#     def unlink(self, cr, uid, ids, context=None):
#         for tmpl in self.browse(cr,uid,ids,context=context):
#             try:
#                     algolia = self.pool.get('algolia.config')
#                     aloglia_ids = algolia.search(cr,uid,[],context=context)
#                     tmpl_obj =  self.pool.get('product.template')
#                     if aloglia_ids and  tmpl.id_algolia :
#                         algolia = algolia.browse(cr, uid, aloglia_ids[0] , context=context) 
#                         client = algoliasearch.client.Client(algolia.client_id_algolia, algolia.api_algolia)
#                         index = client.initIndex(algolia.index_algolia)
#                         res = index.delete_object(tmpl.id_algolia)
#             except:
#                 pass
#         return super(product_template, self).unlink(cr, uid, ids, context=context)