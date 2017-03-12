{
    "name" : "CSAP Machine",
    "version" : "1.0",
    "author" : "Cycom Software Development",
    "category": 'Custom Modules',
    'summary': 'Machine connection to Ultramatic Device Alg ZK10',
    "description": """
    Modul ini adalah sub modul dari Attendance and Payroll CycomERP. Logaritma yang digunakan dikenal dengan ZK10.
    Sub modul ini dikembangkan oleh Mario Ardi & Nicholas Kotama dengan bantuan AlSayed Gamal dari MENA Commerce Mesir.
    Copyright © 2016 by Cycom Software Development, Indonesia.
    """,
    'website': 'http://www.cycomsoft.com',    
    'depends': ['hr','base','csap_attendance'],
    'data': [
        'csap_machine.xml',
    ],
    'installable': True,
    'auto_install': False,    
}
