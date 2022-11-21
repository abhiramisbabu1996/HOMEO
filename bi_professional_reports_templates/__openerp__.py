# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
{
    'name': 'Professional Report Templates',
    'version': '8.0.0.0',
    'category': 'Tools',
    'summary': '',
    'description': """
	Customize report, customize pdf report, customize template report, Customize Sales Order report,Customize Purchase Order report, 			Customize invoice report, Customize delivery Order report, Accounting Reports, Easy reports, Flexible report,Fancy Report temp, Pdf reports, Report template, good design reports.
    """,
    'license':'AGPL-3',
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    'depends': ['base', 'account', 'sale', 'purchase', 'stock', 'base_vat'],
    'data': [
		"res_company.xml",
        
        "invoice_report/custom_report_account.xml",
        "invoice_report/custom_report_invoice_document.xml",

        "delivery_report/custom_stock_report.xml",
        "delivery_report/custom_report_deliveryslip_document.xml",

        "purchase_report/custom_purchase_report.xml",
        "purchase_report/custom_report_purchaseorder_document.xml",
        "purchase_report/custom_report_purchasequotation_document.xml",

        "sale_report/custom_sale_report.xml",
        "sale_report/custom_report_saleorder_document.xml",
     ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/_aihFWW4a5E',
	"images":['static/description/Banner.png'],


}
