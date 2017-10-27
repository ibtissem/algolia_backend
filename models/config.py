# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    #add api credentials  to configuration
    api_algolia = fields.Char(related='website_id.api_algolia')
    client_id_algolia = fields.Char(related='website_id.client_id_algolia')
    index_algolia = fields.Char(related='website_id.index_algolia')
    
    @api.model
    def get_values(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res = super(ResConfigSettings, self).get_values()  
        website = self.env['website'].search([])
        if website:
            res.update(
                api_algolia = website[0].api_algolia,
                client_id_algolia = website[0].client_id_algolia,
                index_algolia = website[0].index_algolia,
            )
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values() 
        set_param = self.env['ir.config_parameter'].sudo().set_param
        website = self.env['website'].search([])
        add = self.api_addressverify
        for wbs in website:
            wbs.write({'api_algolia': self.api_algolia,'client_id_algolia': self.client_id_algolia,'index_algolia': self.index_algolia})
