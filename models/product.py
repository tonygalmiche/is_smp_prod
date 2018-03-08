# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_matiere   = fields.Char("Matière")
    is_categorie = fields.Char('Catégorie')







