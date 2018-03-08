# -*- coding: utf-8 -*-
from openerp import models,fields,api


class is_machine(models.Model):
    _name='is.machine'
    _order='name desc'

    name               = fields.Char("N°Machine", required=True)
    client_id          = fields.Many2one('res.partner', 'Client', domain=[('is_company','=',True),('customer','=',True)])
    affaire            = fields.Char("Affaire")
    date_creation      = fields.Date("Date création")
    date_livraison     = fields.Date("Date livraison prévue")
    commentaire        = fields.Text("Commentaire")
    sous_ensemble_ids  = fields.One2many('is.sous.ensemble', 'machine_id', u'Sous-ensembles', readonly=True)



