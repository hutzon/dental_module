from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestDentalAppointment(TransactionCase):

    def setUp(self):
        super(TestDentalAppointment, self).setUp()
        self.doctor = self.env['res.partner'].create({
            'name': 'Dr. Test',
            'is_doctor': True,
        })
        self.patient = self.env['res.partner'].create({
            'name': 'Patient Test',
            'is_patient': True,
        })
        self.Appointment = self.env['dental.appointment']

    def test_appointment_end_date_computation(self):
        """Test that end date is correctly computed based on duration."""
        start_time = datetime.now().replace(second=0, microsecond=0)
        appointment = self.Appointment.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'date_start': start_time,
            'duration': 1.0,  # 1 hour
        })
        expected_end = start_time + timedelta(hours=1)
        self.assertEqual(appointment.date_end, expected_end, "End date should be 1 hour after start date")

    def test_double_booking_prevention(self):
        """Test that overlapping appointments for the same doctor are prevented."""
        start_time = datetime.now().replace(second=0, microsecond=0)
        
        # Create first appointment
        self.Appointment.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'date_start': start_time,
            'duration': 1.0,
        })

        # Try to create overlapping appointment
        with self.assertRaises(ValidationError):
            self.Appointment.create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'date_start': start_time + timedelta(minutes=30),  # Starts 30 mins later, overlaps
                'duration': 1.0,
            })
            
    def test_non_overlapping_appointment(self):
        """Test that non-overlapping appointments are allowed."""
        start_time = datetime.now().replace(second=0, microsecond=0)
        
        # Create first appointment (1 hour long)
        self.Appointment.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'date_start': start_time,
            'duration': 1.0,
        })
        
        # Create second appointment start right after first one
        second_appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'date_start': start_time + timedelta(hours=1),
            'duration': 1.0,
        })
        self.assertTrue(second_appt.id, "Should allow non-overlapping appointment")
