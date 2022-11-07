
{
    'name': "Responsible Person Sale History",

    'summary': """Responsible Person Sale History
        """,


    'description': """
        Responsible Person Sale History.
    """,

    'author': "Hiworth Solutions",
    'website': "http://www.hiworthsolutions.com",
    'license': "AGPL-3",

    'category': 'Sales',
    'version': '8.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['sale','report_xlsx'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
        'report/tax_report_view.xml',
        'report/tax_report_excel.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
}
