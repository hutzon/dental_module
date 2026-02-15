/** @odoo-module **/

import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart, onMounted, useRef } from "@odoo/owl";

export class DentalDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            kpi: {},
            charts: {},
            recent_appointments: [],
            service_types: [],
            filters: {
                date_start: null,
                date_end: null,
                service_type_id: null,
            },
        });
        
        this.pieChartRef = useRef("pieChart");
        this.barChartRef = useRef("barChart");

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
            await this.loadServiceTypes();
            await this.loadData();
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    async loadServiceTypes() {
        this.state.service_types = await this.orm.searchRead("dental.service.type", [], ["id", "name"]);
    }

    async loadData() {
        const result = await this.orm.call("dental.dashboard", "get_dashboard_data", [], {
            date_start: this.state.filters.date_start,
            date_end: this.state.filters.date_end,
            service_type_id: this.state.filters.service_type_id,
        });
        
        this.state.kpi = result.kpi;
        this.state.charts = result.charts;
        this.state.recent_appointments = result.recent_appointments;
        
        this.renderCharts();
    }

    async onFilterChange(ev) {
        const { name, value } = ev.target;
        this.state.filters[name] = value;
        await this.loadData();
    }

    renderCharts() {
        if (!this.state.charts || !this.state.charts.pie || !this.state.charts.bar) return;

        // Destroy existing charts
        if (this.pieChartInstance) this.pieChartInstance.destroy();
        if (this.barChartInstance) this.barChartInstance.destroy();

        // Pie Chart
        if (this.pieChartRef.el) {
            this.pieChartInstance = new Chart(this.pieChartRef.el, {
                type: 'doughnut',
                data: {
                    labels: this.state.charts.pie.labels,
                    datasets: [{
                        label: 'Service Types',
                        data: this.state.charts.pie.data,
                        backgroundColor: [
                            '#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#4bc0c0',
                            '#9966ff', '#ff9f40', '#00d2ff', '#71639e', '#e7e7e7'
                        ],
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: { display: true, text: 'Appointments by Service Type' }
                    }
                }
            });
        }

        // Bar Chart
        if (this.barChartRef.el) {
            this.barChartInstance = new Chart(this.barChartRef.el, {
                type: 'bar',
                data: {
                    labels: this.state.charts.bar.labels,
                    datasets: [{
                        label: 'Appointments',
                        data: this.state.charts.bar.data,
                        backgroundColor: '#36a2eb',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    },
                    plugins: {
                        legend: { display: false },
                        title: { display: true, text: 'Appointments by Doctor' }
                    }
                }
            });
        }
    }
}

DentalDashboard.template = "dental_management.DentalDashboard";
registry.category("actions").add("dental_management.dashboard", DentalDashboard);
