from odoo import models, fields, api
from datetime import datetime, timedelta

class DentalDashboard(models.Model):
    _name = 'dental.dashboard'
    _description = 'Dental Dashboard Helper'

    @api.model
    def get_dashboard_data(self, date_start=None, date_end=None, service_type_id=None):
        """ Returns data for the dashboard charts and KPIs """
        
        # 1. KPI Data
        # We need counts for Pending and Completed regardless of the domain? No, let's keep all KPIs filtered by the date and service type.
        # But wait, original domain was only searching 'done' appointments! Let's change the domain to get everything and then filter for the counts.
        domain = []
        if date_start:
            domain.append(('date_start', '>=', date_start))
        if date_end:
            domain.append(('date_start', '<=', date_end))
        if service_type_id:
            service_type_id = int(service_type_id)
            services_of_type = self.env['dental.service'].search([('service_type_id', '=', service_type_id)])
            if services_of_type:
                domain.append(('service_ids', 'in', services_of_type.ids))

        all_filtered_appointments = self.env['dental.appointment'].search(domain)
        
        # Now segment them
        completed_appointments = all_filtered_appointments.filtered(lambda a: a.state == 'done')
        pending_appointments = all_filtered_appointments.filtered(lambda a: a.state in ['draft', 'confirmed'])

        total_completed = len(completed_appointments)
        total_pending = len(pending_appointments)
        total_appointments = len(all_filtered_appointments)
        patients_seen = len(set(completed_appointments.mapped('patient_id')))
        total_revenue = sum(sum(app.service_ids.mapped('price')) for app in completed_appointments)

        # 2. Charts Data
        service_type_counts = {}
        all_types = self.env['dental.service.type'].search([])
        for t in all_types:
            service_type_counts[t.name] = 0
        service_type_counts['Other'] = 0
        
        # Usually we only want to chart completed appointments, right? Or all? Let's chart all filtered appointments.
        for app in all_filtered_appointments:
            for service in app.service_ids:
                t_name = service.service_type_id.name if service.service_type_id else 'Other'
                if t_name in service_type_counts:
                    service_type_counts[t_name] += 1
                else:
                    service_type_counts[t_name] = 1
                    
        pie_labels = list(service_type_counts.keys())
        pie_data = list(service_type_counts.values())

        doctor_counts = {}
        for app in all_filtered_appointments:
            d_name = app.doctor_id.name
            doctor_counts[d_name] = doctor_counts.get(d_name, 0) + 1
            
        bar_labels = list(doctor_counts.keys())
        bar_data = list(doctor_counts.values())

        # 3. Recent 5 Appointments (Completed)
        recent_appointments = []
        done_domain = domain + [('state', '=', 'done')]
        recent_apps = self.env['dental.appointment'].search(done_domain, order='date_start desc', limit=5)
        for app in recent_apps:
            recent_appointments.append({
                'id': app.id,
                'name': app.name,
                'patient': app.patient_id.name,
                'doctor': app.doctor_id.name,
                'date': app.date_start,
                'services': ", ".join(app.service_ids.mapped('name')),
            })

        return {
            'kpi': {
                'total_appointments': total_appointments,
                'patients_seen': patients_seen,
                'total_revenue': total_revenue,
                'total_pending': total_pending,
                'total_completed': total_completed,
            },
            'charts': {
                'pie': {'labels': pie_labels, 'data': pie_data},
                'bar': {'labels': bar_labels, 'data': bar_data},
            },
            'recent_appointments': recent_appointments,
        }

    def _empty_dashboard_data(self):
         return {
            'kpi': {'total_appointments': 0, 'patients_seen': 0, 'total_revenue': 0, 'total_pending': 0, 'total_completed': 0},
            'charts': {'pie': {'labels': [], 'data': []}, 'bar': {'labels': [], 'data': []}},
            'recent_appointments': [],
        }
