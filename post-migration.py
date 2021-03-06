# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# In post migration script:
# - we can access the registry
# - the new fields are created
# - the old fields are still readable
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        aiico = env['account.invoice.import.config']
        ipo = env['ir.property']

        for config in aiico.search([]):
            value_ref = 'account.invoice.import.config,%d' % config.id
            props = ipo.search([
                ('name', '=', 'invoice_import_id'),
                ('type', '=', 'many2one'),
                ('value_reference', '=', value_ref),
                ('company_id', '=', config.company_id.id),
                ('res_id', '=like', 'res.partner,%'),
                ])
            if props and props[0].res_id:
                res_id_split = props[0].res_id.split(',')
                try:
                    partner_id = int(res_id_split[1])
                except:
                    continue
                config.partner_id = partner_id

# Explications :
# Il faut créer un sous-répertoire "migrations/7.0.0.2/" et mettre ce script dedans:
# le script sera alors exécuté pour openerp 7.0, quand on met à jour le module vers la version 0.2 (pour les numéros de version type '10.0.1.0.2', pas besoin de préfixer le nom du sous-répertoire avec le numéro de version majeur d'Odoo... elle est déjà dans le numéro lui-même)
