# -*- coding: utf-8 -*-
from openerp import models, fields, api, _ 
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