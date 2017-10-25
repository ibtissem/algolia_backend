# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    #add api credentials  to configuration
    api_algolia = fields.Char(related='website_id.api_algolia')
    client_id_algolia = fields.Char(related='website_id.client_id_algolia')
    index_algolia = fields.Char(related='website_id.index_algolia')
    
    @api.model
    def get_default_alias_prefix(self, fields):
        website_obj = self.env['website']
        website = website_obj.search([])
        if website:
            return {'api_algolia': website[0].api_algolia ,'client_id_algolia': website[0].client_id_algolia,'index_algolia': website[0].index_algolia}
 
    @api.multi
    def set_default_alias_prefix(self):
        website_obj = self.env['website']
        for record in self:
            websites = website_obj.search([])
            for website in websites:
                website.write({'api_algolia': record.api_algolia ,'client_id_algolia': record.client_id_algolia,'index_algolia': record.index_algolia})
        return True