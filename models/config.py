# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    def _default_algolia(self):
        return self.env['algolia.config'].search([], limit=1)

    algolia_id = fields.Many2one('algolia.config', string="Algolia", default=_default_algolia, required=True)
    api_algolia = fields.Char(related='algolia_id.api_algolia')
    client_id_algolia = fields.Char(related='algolia_id.client_id_algolia')
    index_algolia = fields.Char(related='algolia_id.index_algolia')
    
#     @api.model
#     def get_default_alias_prefix(self, fields):
#         algolia_obj = self.env['algolia.config']
#         algolia = algolia_obj.
#         return {'alias_prefix': alias.alias_name if alias else False}
# 
#     @api.multi
#     def set_default_alias_prefix(self):
#         for record in self:
#             alias = self._find_default_lead_alias_id()
#             if alias:
#                 alias.write({'alias_name': record.alias_prefix})
#             else:
#                 self.env['mail.alias'].with_context(alias_model_name='crm.lead', alias_parent_model_name='crm.team').create({'alias_name': record.alias_prefix})
# 
#         return True