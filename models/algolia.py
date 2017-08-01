# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import fields, osv, expression
try:
    import algoliasearch
except ImportError:
    _logger.debug('Can not import algoliasearch')
    
class ip_algolia(osv.osv): 
    _name = "ip.algolia"   
    
    _columns = {
                'name': fields.char('Nom'),
                'ip_api_algolia': fields.char('Api Key Algolia'),
                'ip_client_id_algolia': fields.char('Algolia identifier'),
                'ip_index_algolia': fields.char('Algolia Index'),
                }
