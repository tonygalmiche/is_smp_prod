# -*- coding: utf-8 -*-

from openerp import models,fields,api


class purchase_order(models.Model):
    _inherit = "purchase.order"


    @api.multi
    def acceder_devis(self):
        for obj in self:
            return {
                'name': u'Devis '+obj.name or '',
                'view_mode': 'form,tree',
                'view_type': 'form',
                'res_model': 'purchase.order',
                'res_id': obj.id,
                'type': 'ir.actions.act_window',
            }




