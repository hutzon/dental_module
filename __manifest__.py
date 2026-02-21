{
    'name': 'Dental Clinic Management',
    'version': '1.0',
    'summary': 'Manage Dental Appointments, Patients, and Doctors',
    'sequence': 10,
    'description': """
Dental Clinic Management
========================
A comprehensive module to manage dental clinic operations:
- **Appointments**: Schedule and manage patient visits with a calendar view.
- **Patients**: Extended contact management with medical history.
- **Doctors**: Manage doctor availabilities and assignments.
    """,
    'category': 'Healthcare',
    'website': '',
    'depends': ['base', 'contacts', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/dental_dashboard_action.xml',
        'views/dental_appointment_views.xml',
        'views/dental_service_type_views.xml',
        'views/dental_service_views.xml',
        'views/dental_prescription_views.xml',
        'reports/prescription_report.xml',
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dental_management/static/src/dashboard/dental_dashboard.js',
            'dental_management/static/src/dashboard/dental_dashboard.xml',
        ],
    },
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
