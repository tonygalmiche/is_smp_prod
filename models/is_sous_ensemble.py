# -*- coding: utf-8 -*-
from openerp import models,fields,api
import tempfile
import base64
import os
import csv
import codecs


class is_sous_ensemble(models.Model):
    _name='is.sous.ensemble'
    _order='name desc'

    name               = fields.Char("Référence", required=True)
    machine_id         = fields.Many2one('is.machine', 'Machine')
    commentaire        = fields.Text("Commentaire")


    @api.multi
    def acceder_sous_ensemble(self):
        for obj in self:
            return {
                'name': u'Sous-ensemble '+obj.name or '',
                'view_mode': 'form,tree',
                'view_type': 'form',
                'res_model': 'is.sous.ensemble',
                'res_id': obj.id,
                'type': 'ir.actions.act_window',
            }


    @api.multi
    def acceder_lignes(self):
        print "Accèder lignes"
        for obj in self:
            return {
                'name': "Lignes",
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'is.sous.ensemble.line',
                'type': 'ir.actions.act_window',
                'domain': [('sous_ensemble_id','=',obj.id)],
            }



    @api.multi
    def importer_nomenclature(self):
        for obj in self:
            print obj

            # ** Recherche si une pièce jointe est déja associèe ***************
            attachment_obj = self.env['ir.attachment']
            model=self._name
            attachments = attachment_obj.search([('res_model','=',model),('res_id','=',obj.id)],order="id desc",limit=1)
            print attachments
            # ******************************************************************

            for attachment in attachments:
                #file_id, file_path = tempfile.mkstemp(suffix='.csv', prefix='import-nomenclature-')
                #print file_id, file_path
                #f = open(file_path,'wb')
                #f.write(attachment.datas.decode('base64'))
                #f.close()
                #os.unlink(path)
                csvfile = base64.decodestring(attachment.datas)
                csvfile = csvfile.split("\n")
                csvfile = csv.reader(csvfile)
                line_obj    = self.env['is.sous.ensemble.line']
                product_obj = self.env['product.product']
                for ct, line in enumerate(csvfile):
                    if ct>0 and len(line)>0:
                        filtre=[
                            ('machine_id'      , '=', obj.machine_id.id),
                            ('sous_ensemble_id', '=', obj.id),
                            ('ordre'           , '=', line[0]),
                        ]
                        print filtre
                        lines = line_obj.search(filtre,order="id desc",limit=1)
                        if len(lines)==0:
                            creation_product=True
                            products = product_obj.search([('default_code','=',line[1])],order="id desc",limit=1)
                            if len(products)>0:
                                product=products[0]
                                creation_product=False
                            if creation_product:
                                vals={
                                    'default_code' : line[1],
                                    'is_matiere'   : unicode(line[2],'utf-8'),
                                    'name'         : unicode(line[3],'utf-8'),
                                    'is_categorie' : unicode(line[5],'utf-8'),
                                    'type'         : 'product',
                                    'list_price'   : 0
                                }
                                product=product_obj.create(vals)
                            vals={
                                'machine_id'       : obj.machine_id.id,
                                'sous_ensemble_id' : obj.id,
                                'ordre'            : line[0],
                                'product_id'       : product.id,
                                'creation_product' : creation_product,
                                'matiere'          : unicode(line[2],'utf-8'),
                                'quantite'         : line[4],
                                'categorie'        : line[5],
                            }
                            res=line_obj.create(vals)
                return self.acceder_lignes()


class is_sous_ensemble_line(models.Model):
    _name='is.sous.ensemble.line'
    _order='machine_id,sous_ensemble_id,ordre,product_id'
    _rec_name='product_id'


    machine_id         = fields.Many2one('is.machine', 'Machine', required=True)
    sous_ensemble_id   = fields.Many2one('is.sous.ensemble', 'Sous-ensemble', required=True)
    ordre              = fields.Integer("Ordre")
    product_id         = fields.Many2one('product.product', 'Référence', domain=[('purchase_ok', '=', True)])
    creation_product   = fields.Boolean("Création",help="Indique si l'article a été créé lors de l'importation",readonly=True)
    matiere            = fields.Char("Matière")
    quantite           = fields.Integer("Quantité")
    categorie          = fields.Char("Catégorie")
    suivi_par          = fields.Char("Suivi par")
    num_dp             = fields.Char("N°DP")
    num_cde            = fields.Char("N°Cde")
    date_cde           = fields.Date("Date Cde")
    delai              = fields.Date("Délai")
    recu_le            = fields.Date("Reçu le")
    code               = fields.Char("Code")
    fournisseur_id     = fields.Many2one('res.partner', 'Fournisseur', domain=[('is_company','=',True),('supplier','=',True)])
    ref_fournisseur    = fields.Char("Réf fournisseur")
    pu_ht              = fields.Float("PU HT")
    total_ht           = fields.Float("Total HT")
    order_ids          = fields.Many2many('purchase.order', 'is_sous_ensemble_line_order_rel', 'line_id','order_id', string="Devis")


    @api.multi
    def creer_devis_action(self):
        partner=self.env['res.partner'].search([],limit=1)[0]
        vals={
            'partner_id'      : partner.id,
            'fiscal_position_id' : partner.property_account_position_id.id,
        }
        order=self.env['purchase.order'].create(vals)
        if order:
            order_line_obj = self.env['purchase.order.line']
            for obj in self:
                vals={
                    'order_id'    : order.id,
                    'product_id'  : obj.product_id.id,
                    'name'        : obj.product_id.name,
                    'product_uom' : obj.product_id.uom_id.id ,
                    'price_unit'  : 0,
                    'product_qty' : obj.quantite,
                    'date_planned': '2018-03-03',
                }
                line=order_line_obj.create(vals)
                obj.order_ids=[(4, order.id)]




