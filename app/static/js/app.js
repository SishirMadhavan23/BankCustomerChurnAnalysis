/**
 * Bank Customer Churn Analysis - Main Application Logic
 * Handles navigation, predictions, dashboard, and chart rendering
 */

// ===== Chart Instances =====
let churnDistChartInstance = null;
let geoDistChartInstance = null;
let ageDistChartInstance = null;
let featureImportanceChartInstance = null;

// ===== Navigation =====
document.addEventListener('DOMContentLoaded', function() {
    // Mobile nav toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    // Smooth scroll for all hash links (nav links, hero buttons, footer links)
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            // Close mobile nav if open
            if (navLinks) {
                navLinks.classList.remove('active');
            }
            // Update active nav link
            document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
            if (this.closest('.nav-links')) {
                this.classList.add('active');
            }
        });
    });
    
    // Highlight active section on scroll
    const sections = document.querySelectorAll('.section[id]');
    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 150;
            if (pageYOffset >= sectionTop) {
                current = section.getAttribute('id');
            }
        });
        document.querySelectorAll('.nav-links a[data-section]').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-section') === current) {
                link.classList.add('active');
            }
        });
    });
    
    // Load dashboard data
    loadDashboard();
    
    // Load hero stats
    loadHeroStats();
});

// ===== Hero Stats =====
async function loadHeroStats() {
    try {
        const response = await fetch('/api/dashboard');
        const result = await response.json();
        if (result.success) {
            document.getElementById('heroChurnRate').textContent = 
                result.data.churn_rate.toFixed(1) + '%';
            document.getElementById('heroTotalCustomers').textContent = 
                result.data.total_customers.toLocaleString();
        }
    } catch (error) {
        console.error('Failed to load hero stats:', error);
    }
}

// ===== Prediction =====
async function submitPrediction(event) {
    event.preventDefault();
    
    const form = document.getElementById('predictForm');
    const btn = document.getElementById('predictBtn');
    const resultCard = document.getElementById('predictResult');
    
    // Disable button and show loading
    btn.disabled = true;
    btn.textContent = getTranslatedText('loading') || 'Loading...';
    
    const formData = {
        credit_score: parseFloat(document.getElementById('creditScore').value),
        geography: document.getElementById('geography').value,
        gender: document.getElementById('gender').value,
        age: parseFloat(document.getElementById('age').value),
        tenure: parseFloat(document.getElementById('tenure').value),
        balance: parseFloat(document.getElementById('balance').value),
        num_products: parseInt(document.getElementById('numProducts').value),
        has_cr_card: parseInt(document.getElementById('hasCrCard').value),
        is_active_member: parseInt(document.getElementById('isActive').value),
        estimated_salary: parseFloat(document.getElementById('salary').value)
    };
    
    try {
        const lang = getCurrentLanguage();
        const response = await fetch(`/api/predict?lang=${lang}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Show result card
            form.style.display = 'none';
            resultCard.style.display = 'block';
            
            // Update gauge
            const gaugeFill = document.getElementById('gaugeFill');
            const gaugeValue = document.getElementById('gaugeValue');
            const riskBadge = document.getElementById('riskBadge');
            const resultMessage = document.getElementById('resultMessage');
            const confidenceValue = document.getElementById('confidenceValue');
            const aiSection = document.getElementById('aiInsights');
            const aiExplanation = document.getElementById('aiExplanation');
            const aiRecommendation = document.getElementById('aiRecommendation');
            const aiRiskFactors = document.getElementById('aiRiskFactors');
            const aiModelBadge = document.getElementById('aiModelBadge');
            
            // Animate gauge
            const probability = result.probability;
            const degrees = (probability / 100) * 360;
            
            setTimeout(() => {
                gaugeFill.style.background = 
                    `conic-gradient(var(--primary) 0deg ${degrees}deg, var(--border) ${degrees}deg 360deg)`;
                gaugeValue.textContent = probability.toFixed(1) + '%';
            }, 100);
            
            // Set risk badge
            if (result.risk_level === 'high') {
                riskBadge.textContent = getTranslatedText('predict_risk_high') || 'High Risk';
                riskBadge.className = 'risk-badge high';
                resultMessage.textContent = (getTranslatedText('predict_risk_high') || 'High Risk');
            } else {
                riskBadge.textContent = getTranslatedText('predict_risk_low') || 'Low Risk';
                riskBadge.className = 'risk-badge low';
                resultMessage.textContent = (getTranslatedText('predict_risk_low') || 'Low Risk');
            }
            
            confidenceValue.textContent = result.confidence.toFixed(1) + '%';
            
            // Display AI insights if available
            if (result.ai && result.ai.ai_available) {
                aiSection.style.display = 'block';
                aiExplanation.textContent = result.ai.explanation || '';
                aiRecommendation.textContent = result.ai.recommendation || '';
                aiRiskFactors.innerHTML = result.ai.risk_factors 
                    ? result.ai.risk_factors.replace(/\n/g, '<br>')
                    : '';
                aiModelBadge.textContent = '🤖 ' + (result.ai.model_used || 'Ollama AI');
            } else {
                aiSection.style.display = 'none';
            }
        } else {
            alert('Error: ' + (result.error || 'Prediction failed'));
        }
    } catch (error) {
        console.error('Prediction error:', error);
        alert('Failed to get prediction. Check the console for details.');
    } finally {
        btn.disabled = false;
        btn.textContent = getTranslatedText('predict_btn') || 'Predict Churn';
    }
    
    return false;
}

function resetPrediction() {
    document.getElementById('predictForm').style.display = 'block';
    document.getElementById('predictResult').style.display = 'none';
    
    // Reset gauge
    const gaugeFill = document.getElementById('gaugeFill');
    gaugeFill.style.background = 'conic-gradient(var(--primary) 0deg, var(--danger) 0deg)';
    document.getElementById('gaugeValue').textContent = '0%';
}

// ===== Dashboard =====
async function loadDashboard() {
    const loadingEl = document.getElementById('dashboardLoading');
    const contentEl = document.getElementById('dashboardContent');
    
    loadingEl.style.display = 'block';
    contentEl.style.display = 'none';
    
    try {
        const lang = getCurrentLanguage();
        const response = await fetch(`/api/dashboard?lang=${lang}`);
        const result = await response.json();
        
        if (result.success) {
            const data = result.data;
            
            // Update KPIs
            document.getElementById('kpiTotal').textContent = data.total_customers.toLocaleString();
            document.getElementById('kpiChurned').textContent = data.churned.toLocaleString();
            document.getElementById('kpiRetained').textContent = data.retained.toLocaleString();
            document.getElementById('kpiChurnRate').textContent = data.churn_rate.toFixed(1) + '%';
            document.getElementById('kpiActive').textContent = data.active_members.toLocaleString();
            document.getElementById('kpiAvgAge').textContent = data.avg_age;
            
            // Render charts
            renderChurnDistChart(data);
            renderGeoDistChart(data);
            renderAgeDistChart(data);
            renderFeatureImportanceChart();
            
            loadingEl.style.display = 'none';
            contentEl.style.display = 'block';
        }
    } catch (error) {
        console.error('Failed to load dashboard:', error);
        loadingEl.innerHTML = '<p>Failed to load dashboard data.</p>';
    }
}

// ===== Chart Rendering Functions =====
function renderChurnDistChart(data) {
    const ctx = document.getElementById('churnDistChart').getContext('2d');
    
    if (churnDistChartInstance) {
        churnDistChartInstance.destroy();
    }
    
    churnDistChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [
                getTranslatedText('dashboard_retained') || 'Retained',
                getTranslatedText('dashboard_churned') || 'Churned'
            ],
            datasets: [{
                data: [data.retained, data.churned],
                backgroundColor: ['#22c55e', '#ef4444'],
                borderColor: ['#1e293b', '#1e293b'],
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 12 },
                        padding: 16
                    }
                }
            },
            animation: {
                animateRotate: true,
                duration: 1200
            }
        }
    });
}

function renderGeoDistChart(data) {
    const ctx = document.getElementById('geoDistChart').getContext('2d');
    
    if (geoDistChartInstance) {
        geoDistChartInstance.destroy();
    }
    
    const geos = Object.keys(data.geo_distribution);
    const counts = Object.values(data.geo_distribution);
    
    geoDistChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: geos,
            datasets: [{
                label: 'Customers',
                data: counts,
                backgroundColor: ['#6366f1', '#a5b4fc', '#8b5cf6'],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#334155' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            },
            animation: {
                duration: 1200
            }
        }
    });
}

function renderAgeDistChart(data) {
    const ctx = document.getElementById('ageDistChart').getContext('2d');
    
    if (ageDistChartInstance) {
        ageDistChartInstance.destroy();
    }
    
    const ages = Object.keys(data.age_distribution);
    const rates = ages.map(age => data.age_distribution[age].rate * 100);
    
    ageDistChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ages,
            datasets: [{
                label: getTranslatedText('dashboard_churn_rate') || 'Churn Rate (%)',
                data: rates,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#ef4444',
                pointBorderColor: '#1e293b',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { size: 12 } }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#334155' },
                    ticks: { 
                        color: '#94a3b8',
                        callback: function(value) { return value + '%'; }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            },
            animation: {
                duration: 1200
            }
        }
    });
}

// ===== Dataset Upload =====
async function uploadDataset(files) {
    if (!files || files.length === 0) return;
    
    const file = files[0];
    const statusEl = document.getElementById('uploadStatus');
    const uploadArea = document.getElementById('uploadArea');
    
    // Show loading
    statusEl.style.display = 'block';
    statusEl.className = 'upload-status loading';
    statusEl.textContent = `Uploading and processing ${file.name}...`;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload-dataset', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (result.success) {
            statusEl.className = 'upload-status success';
            statusEl.textContent = result.message || `✅ ${result.total} customers processed! ${result.churned} at risk of churn.`;
            
            // Reload dashboard with new data
            loadDashboard();
            
            // Reset file input
            document.getElementById('datasetFile').value = '';
        } else {
            statusEl.className = 'upload-status error';
            statusEl.textContent = '❌ ' + (result.error || 'Upload failed');
        }
    } catch (error) {
        statusEl.className = 'upload-status error';
        statusEl.textContent = '❌ Failed to upload file. Is the server running?';
        console.error('Upload error:', error);
    }
}

// Drag and drop support
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
        ['dragenter', 'dragover'].forEach(event => {
            uploadArea.addEventListener(event, function(e) {
                e.preventDefault();
                e.stopPropagation();
                this.classList.add('dragover');
            });
        });
        ['dragleave', 'drop'].forEach(event => {
            uploadArea.addEventListener(event, function(e) {
                e.preventDefault();
                e.stopPropagation();
                this.classList.remove('dragover');
            });
        });
        uploadArea.addEventListener('drop', function(e) {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                document.getElementById('datasetFile').files = files;
                uploadDataset(files);
            }
        });
    }
});

// ===== Customer Search =====
let searchDebounceTimer = null;

async function searchCustomers() {
    const query = document.getElementById('customerSearchInput').value.trim();
    const geo = document.getElementById('customerGeoFilter').value;
    const status = document.getElementById('customerStatusFilter').value;
    const loadingEl = document.getElementById('customersLoading');
    const tableContainer = document.getElementById('customersTableContainer');
    const tableBody = document.getElementById('customersTableBody');
    const countEl = document.getElementById('customerCount');

    // If no query, show all customers filtered by geo/status
    const endpoint = query
        ? `/api/customers/search?q=${encodeURIComponent(query)}&geo=${geo}&status=${status}`
        : `/api/customers?geo=${geo}&status=${status}`;

    loadingEl.style.display = 'block';
    tableContainer.style.display = 'none';

    try {
        const response = await fetch(endpoint);
        const result = await response.json();

        loadingEl.style.display = 'none';

        if (result.success && result.customers && result.customers.length > 0) {
            tableBody.innerHTML = '';
            result.customers.forEach(c => {
                const statusClass = c.exited === 1 ? 'status-churned' : 'status-retained';
                const statusText = c.exited === 1 ? '🔴 Churned' : '🟢 Retained';
                const activeText = c.is_active_member === 1 ? '✅ Yes' : '❌ No';
                const balanceFormatted = '$' + c.balance.toLocaleString('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0});

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>${c.name}</strong></td>
                    <td>${c.age}</td>
                    <td>${c.geography}</td>
                    <td>${c.credit_score}</td>
                    <td>${balanceFormatted}</td>
                    <td>${c.num_products}</td>
                    <td>${activeText}</td>
                    <td>${c.tenure} yrs</td>
                    <td><span class="${statusClass}">${statusText}</span></td>
                `;
                tableBody.appendChild(row);
            });
            countEl.textContent = `${result.total} customer${result.total !== 1 ? 's' : ''} found`;
            tableContainer.style.display = 'block';
        } else {
            tableBody.innerHTML = `<tr><td colspan="9" class="no-results">No customers found matching "${query || 'all filters'}"</td></tr>`;
            countEl.textContent = '0 customers';
            tableContainer.style.display = 'block';
        }
    } catch (error) {
        console.error('Search error:', error);
        loadingEl.style.display = 'none';
        tableBody.innerHTML = '<tr><td colspan="9" class="no-results">Failed to load customers. Is the server running?</td></tr>';
        tableContainer.style.display = 'block';
    }
}

// Search on Enter key
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('customerSearchInput');
    if (searchInput) {
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchCustomers();
            }
        });
    }
});

async function renderFeatureImportanceChart() {
    const ctx = document.getElementById('featureImportanceChart').getContext('2d');
    
    if (featureImportanceChartInstance) {
        featureImportanceChartInstance.destroy();
    }
    
    try {
        const response = await fetch('/api/feature-importances');
        const result = await response.json();
        
        if (result.success) {
            const features = result.data.map(d => d.feature);
            const importances = result.data.map(d => d.importance * 100);
            
            featureImportanceChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: features,
                    datasets: [{
                        label: 'Importance (%)',
                        data: importances,
                        backgroundColor: [
                            '#6366f1', '#8b5cf6', '#a855f7', '#d946ef',
                            '#ec4899', '#f43f5e', '#ef4444', '#f97316',
                            '#eab308', '#22c55e'
                        ],
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            grid: { color: '#334155' },
                            ticks: { 
                                color: '#94a3b8',
                                callback: function(value) { return value.toFixed(1) + '%'; }
                            }
                        },
                        y: {
                            grid: { display: false },
                            ticks: { color: '#94a3b8' }
                        }
                    },
                    animation: {
                        duration: 1200
                    }
                }
            });
        }
    } catch (error) {
        console.error('Failed to load feature importances:', error);
    }
}