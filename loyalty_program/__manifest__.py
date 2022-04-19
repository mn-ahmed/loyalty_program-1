# -*- coding: utf-8 -*-
{
    'name': "Loyalty Program for Sale Odoo Apps",

    'summary': """
        This module loyalty Program for sales odoo is used to give Sale loyalty redemption points for every sale to your customers from there screen.
        
        """,

    'description': """
        This module loyalty Program for sales odoo is used to give Sale loyalty redemption points for every sale to your customers from there screen.
        Customer can also redeem this loyalty points for other sale from there screen. 
        Every single purchase from the Sale, records the Loyalty Rewards based on configuration setup on there backend and those rewards
         will be redeemed on Sale,POS and Website order from screen order easily. 
         Reward redeems visible on applied Sale order so it will be helpful for see history of the reward point redemption. 
         When customer is cancelled order that time history will also get cancelled so no loyalty point calculated.     
    """,
    'category': 'sale',
    'version': '14.0.0.1',
	'license': 'AGPL-3',
	'author': 'medconsultantweb@gmail.com',
	'website': 'https://www.weblemon.org',
	'category': 'Sales',
	'price': '55.0',
    'currency': 'USD',
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_coupon'],

    # always loaded
    'data': [
        'data/loyalty_product.xml',
        'data/loyalty_level.xml',
        'security/ir.model.access.csv',
        'views/loyalty_email_template.xml',
        'views/res_config_settings_views.xml',
        'views/loyalty_program_views.xml',
        'views/res_partner_view.xml',
        'views/loyalty_history_views.xml',
        'views/partner_level_views.xml',
        'views/sale_order_views.xml',
        'views/menus.xml',
        'wizards/wizard_loyalty_point.xml',
    ],

    'demo': [
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/image1.jpg']
}
