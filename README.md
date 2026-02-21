# Dental Clinic Management for Odoo 18

**Dental Clinic Management** is a comprehensive Odoo module designed to streamline the daily operations of a dental clinic. It provides a professional interface for managing appointments, patients, doctors, and medical history, all centered around a dynamic dashboard.

## 🌟 Key Features

### 📊 Dynamic Dashboard
- **Real-time Overview**: View total pending appointments, completed appointments, patients seen, and revenue at a glance.
- **Interactive Charts**:
    - **Service Distribution**: Visual Pie Chart showing appointments by service type.
    - **Doctor Performance**: Bar Chart comparing appointment counts by doctor.
- **Smart Filters**: Filter the entire dashboard by **Date Range** and **Service Type** (e.g., Orthodontics, Surgery).
- **Recent Activity**: detailed list of the last 5 completed appointments.

### 📅 Appointment Management
- **Calendar-First Design**: Intuitive calendar view for scheduling with **Status Color Coding** (Draft = Grey, Confirmed = Blue, Done = Green, Canceled = Red).
- **Kanban View**: Visual cards with status color indicators.
- **Double-Booking Prevention**: Automatic validation prevents scheduling conflicts for doctors.
- **Service Integration**: Select multiple services for each appointment; duration is calculated automatically.
- ** Status Workflow**: Track appointments from Draft -> Confirmed -> Done, with options to Cancel.

### 📝 Medical Prescriptions
- **Integrated Creation**: Generate prescriptions directly from an appointment with one click (auto-fills patient and doctor info).
- **Medication Details**: Register medication name, dosage, frequency, and duration.
- **PDF Generation**: Instantly print or download a professional PDF prescription ready for the patient.

### 🦷 Service Management
- **Service Types**: Organize services into categories (e.g., General Dentistry, Orthodontics, Cosmetic).
- **Service Catalog**: Define services with standard prices and durations.

### 📂 Patient & Medical History
- **Specialized Contact View**: "Is Patient" flag distinguishes clients from other contacts.
- **Medical History**:
    - **Automated Logging**: History records are automatically created when appointments are marked as "Done".
    - **Next Appointment**: Quickly view the patient's next scheduled visit directly on their profile.
    - **Manual Entries**: Add specific medical notes or past history manually.

### 👨‍⚕️ Doctor Management
- **Doctor Profiles**: Dedicated "Is Doctor" flag.
- **Workload Visualization**: See appointments assigned to specific doctors in the dashboard.

## 🛠 Installation & Configuration

1.  **Install**: Locate the module `dental_management` in your Odoo Apps list and click **Activate**.
2.  **Define Service Types**:
    - Go to `Dental Clinic > Configuration > Service Types`.
    - Create categories like *Orthodontics*, *Pediatric*, *Surgery*.
3.  **Define Services**:
    - Go to `Dental Clinic > Configuration > Services`.
    - Create services (e.g., *Root Canal*, *Cleaning*) and link them to a Type.

## 🚀 Usage Workflow

1.  **Open the App**: You land immediately on the **Dashboard**.
2.  **Schedule**: Go to *Appointments*, click a calendar slot, select Patient, Doctor, and Services.
3.  **Perform**: When the visit is over, open the appointment and click **Mark as Done**.
4.  **Review**: Go to *Patients*, find the client, and check the **Medical History** tab to see the automated entry and their next appointment.

## 📋 Requirements
- Odoo 18.0
- Depends on: `base`, `contacts`, `calendar`

## 👤 Author
Developed for **BlueHat**.
