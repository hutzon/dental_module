from odoo import models, fields, api
from datetime import datetime, timedelta

class DentalDashboard(models.Model):
    _name = 'dental.dashboard'
    _description = 'Dental Dashboard Helper'

    @api.model
    def get_dashboard_data(self, date_start=None, date_end=None, service_type_id=None):
        """ Returns data for the dashboard charts and KPIs """
        
        # Domain construction
        domain = [('state', '=', 'done')]
        if date_start:
            domain.append(('date_start', '>=', date_start))
        if date_end:
            domain.append(('date_start', '<=', date_end))
        
        # If filtering by service type, we need to handle Many2many
        # This is a bit tricky since appointments have multiple services
        # We'll filter appointments that have AT LEAST one service of the given type
        if service_type_id:
            service_type_id = int(service_type_id)
            services_of_type = self.env['dental.service'].search([('service_type_id', '=', service_type_id)])
            if services_of_type:
                domain.append(('service_ids', 'in', services_of_type.ids))
            else:
                # If no services of this type exist, logically no appointments match
                return self._empty_dashboard_data()

        appointments = self.env['dental.appointment'].search(domain)
        
        # 1. KPI Data
        total_appointments = len(appointments)
        patients_seen = len(set(appointments.mapped('patient_id')))
        # Revenue: Sum of prices of all services in these appointments
        # Note: If an appointment has multiple services, we sum them all.
        # If we filtered by Service Type, should we only sum services of that type?
        # User requirement: "General information... dynamic updates". 
        # Usually dashboard logic keeps context. Let's sum all services of the MATCHED appointments for simplicity mostly,
        # but technically accurate would be to filter services too. 
        # For now, let's sum total revenue of the appointments found.
        total_revenue = sum(sum(app.service_ids.mapped('price')) for app in appointments)

        # 2. Charts Data
        
        # Pie Chart: Appointments by Service Type
        # Logic: Iterate appointments, count occurrences of Service Types. 
        # An appointment with 2 types counts for both? Yes, usually.
        service_type_counts = {}
        all_types = self.env['dental.service.type'].search([])
        for t in all_types:
            service_type_counts[t.name] = 0
            
        # Also handle "Undefined" type
        service_type_counts['Other'] = 0
        
        for app in appointments:
            for service in app.service_ids:
                t_name = service.service_type_id.name if service.service_type_id else 'Other'
                if t_name in service_type_counts:
                    service_type_counts[t_name] += 1
                else:
                    service_type_counts[t_name] = 1 # Should cover 'Other' initialization
                    
        # Remove zero counts to clean up chart? Or keep top 5?
        # Let's keep all for now, assuming not too many types.
        pie_labels = list(service_type_counts.keys())
        pie_data = list(service_type_counts.values())

        # Bar Chart: Appointments by Doctor
        doctor_counts = {}
        for app in appointments:
            d_name = app.doctor_id.name
            doctor_counts[d_name] = doctor_counts.get(d_name, 0) + 1
            
        bar_labels = list(doctor_counts.keys())
        bar_data = list(doctor_counts.values())

        # 3. Recent 5 Appointments
        recent_appointments = []
        # Re-search with limit and order, but using same domain
        recent_apps = self.env['dental.appointment'].search(domain, order='date_start desc', limit=5)
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
            },
            'charts': {
                'pie': {'labels': pie_labels, 'data': pie_data},
                'bar': {'labels': bar_labels, 'data': bar_data},
            },
            'recent_appointments': recent_appointments,
        }

    def _empty_dashboard_data(self):
         return {
            'kpi': {'total_appointments': 0, 'patients_seen': 0, 'total_revenue': 0},
            'charts': {'pie': {'labels': [], 'data': []}, 'bar': {'labels': [], 'data': []}},
            'recent_appointments': [],
        }
