{
    'name': 'Employee Leave Application',
    'version': '1.0',
    'summary': 'Allow employees to apply for leave using their ID number.',
    'author': 'James Oginga',
    'category': 'Human Resources',
    'depends': ['hr', 'website'],
    'data': [
        'views/employee_leave_view.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': False,
}
