# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import fields, osv, expression 
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
    
class product_template(osv.osv): 
    _inherit = "product.template"   
    
    _columns = {
                'ip_aded_algolia': fields.boolean('Aded to algolia'),
                'id_algolia': fields.char('Id Produit Algolia'),
                }

    def create(self, cr, uid, values, context=None):
            res = super(product_template, self).create(cr,uid,values,context=context)
            tmpl = self.browse(cr,uid,res,context=context) 
            if tmpl:
                try:
                    algolia = self.pool.get('ip.algolia')
                    aloglia_ids = algolia.search(cr,uid,[],context=context)
                    tmpl_obj =  self.pool.get('product.template')
                    objects = []
                    if aloglia_ids:
                        algolia = algolia.browse(cr, uid, aloglia_ids[0] , context=context) 
                        client = algoliasearch.client.Client(algolia.ip_client_id_algolia, algolia.ip_api_algolia)
                        index = client.initIndex(algolia.ip_index_algolia)
                        object =  {
                                            'id_odoo':tmpl.id,
                                            'name_product':tmpl.name,
                                            'description_product':tmpl.ip_title,
                                            'image_product':tmpl.image_medium,
                                            'prix':tmpl.ip_min_price,
#                                             'ip_url':tmpl.ip_prod_url,
                                            'ref_interne':tmpl.ip_ref_interne,
                                            } 
                        algolia_res = index.addObject(object)
                        objectID = algolia_res["objectID"]
                        if objectID:
                            self.write(cr,uid,res,{'ip_aded_algolia':True,'id_algolia':objectID})
                except:
                    pass
            return res   

    def write(self, cr, uid, ids, values, context=None):
        if ids:
            if isinstance(ids, (int, long)):
              ids = [ids]
            res = super(product_template, self).write(cr,uid,ids,values,context=context)
            tmpl = self.browse(cr,uid,ids[0],context=context) 
            if tmpl:
                try:
                    algolia = self.pool.get('ip.algolia')
                    aloglia_ids = algolia.search(cr,uid,[],context=context)
                    tmpl_obj =  self.pool.get('product.template')
                    if aloglia_ids and  tmpl.id_algolia:
                        algolia = algolia.browse(cr, uid, aloglia_ids[0] , context=context) 
                        client = algoliasearch.client.Client(algolia.ip_client_id_algolia, algolia.ip_api_algolia)
                        index = client.initIndex(algolia.ip_index_algolia)
                        index.partial_update_object({
                                            'id_odoo':tmpl.id,
                                            'name_product':tmpl.name,
                                            'description_product':tmpl.ip_title,
                                            'image_product':tmpl.image_medium,
                                            'prix':tmpl.ip_min_price,
#                                             'ip_url':tmpl.ip_prod_url or '',
                                            'ref_interne':tmpl.ip_ref_interne,
                                            'objectID':tmpl.id_algolia or 0
                                            })
                except:
                    pass
        return res  
        
    def unlink(self, cr, uid, ids, context=None):
        for tmpl in self.browse(cr,uid,ids,context=context):
            try:
                    algolia = self.pool.get('ip.algolia')
                    aloglia_ids = algolia.search(cr,uid,[],context=context)
                    tmpl_obj =  self.pool.get('product.template')
                    if aloglia_ids and  tmpl.id_algolia :
                        algolia = algolia.browse(cr, uid, aloglia_ids[0] , context=context) 
                        client = algoliasearch.client.Client(algolia.ip_client_id_algolia, algolia.ip_api_algolia)
                        index = client.initIndex(algolia.ip_index_algolia)
                        res = index.delete_object(tmpl.id_algolia)
            except:
                pass
        return super(product_template, self).unlink(cr, uid, ids, context=context)