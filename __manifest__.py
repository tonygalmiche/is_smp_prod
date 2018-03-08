# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo pour SMP Packaging - Production',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
InfoSaône - Module Odoo pour SMP Packaging - Production
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'document',
        'product',
        'purchase',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/is_machine_view.xml',
        'views/is_sous_ensemble_view.xml',
        'views/product_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

