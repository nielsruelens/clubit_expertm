{
    'name': 'clubit_expertm',
    'version': '1.0',
    'category': 'Accounting',
    'description': "Expert/M EDI integration",
    'author': 'Niels Ruelens',
    'website': 'http://clubit.be',
    'summary': "Creates an EDI integration with Expert/M software",
    'sequence': 9,
    'depends': [
        'account',
        'clubit_tools',
    ],
    'data': [
        'partner.xml',
        'tax.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'css': [
    ],
    'images': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}