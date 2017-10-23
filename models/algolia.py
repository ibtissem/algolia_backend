# -*- coding: utf-8 -*-
from openerp import models, fields, api, _ 
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
    
class algolia(models.Model): 
    _name = "algolia.config"   
    
    name = fields.Char('Nom')
    api_algolia = fields.Char('Api Key Algolia')
    client_id_algolia = fields.Char('Algolia identifier')
    index_algolia = fields.Char('Algolia Index')

    @api.model
    def create(self,vals):
        res = super(algolia,self).create(vals)
        self.synchronise_algolia_index()
        return res