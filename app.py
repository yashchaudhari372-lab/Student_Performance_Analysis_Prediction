import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

MODEL_PATH = 'model.pkl'

# Load the trained SVC model
model = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"Error loading {MODEL_PATH}: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduPulse AI | Student Performance Analytics</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-base: #090d16;
            --bg-surface: #111827;
            --bg-surface-elevated: #1a2234;
            --border-subtle: #1f293d;
            --border-active: #3b82f6;
            --brand-primary: #4f46e5;
            --brand-gradient: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
            --accent-green: #10b981;
            --accent-red: #f43f5e;
            --text-heading: #f8fafc;
            --text-body: #94a3b8;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg-base);
            color: var(--text-heading);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Top Navigation Bar */
        .topbar {
            height: 70px;
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: var(--brand-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            color: #ffffff;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
        }

        .brand-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.3px;
        }

        .brand-badge {
            font-size: 0.72rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            background: rgba(79, 70, 229, 0.15);
            color: #818cf8;
            border: 1px solid rgba(129, 140, 248, 0.3);
            text-transform: uppercase;
        }

        .system-status {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            color: var(--text-body);
        }

        .status-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 10px var(--accent-green);
        }

        .status-dot.offline {
            background: #f59e0b;
            box-shadow: 0 0 10px #f59e0b;
        }

        /* Main Viewport Container */
        .dashboard-wrapper {
            max-width: 1440px;
            width: 100%;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 460px 1fr;
            gap: 2rem;
            flex: 1;
        }

        @media (max-width: 1100px) {
            .dashboard-wrapper {
                grid-template-columns: 1fr;
            }
        }

        /* Glass Panel Blocks */
        .glass-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 1.75rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        }

        .panel-header {
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .panel-header h2 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-heading);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .panel-header p {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 4px;
        }

        /* Input Controls */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .form-field {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .form-field.full {
            grid-column: span 2;
        }

        label {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-body);
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }

        input, select {
            width: 100%;
            background: var(--bg-surface-elevated);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 0.75rem 0.9rem;
            color: #ffffff;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s ease;
        }

        input:focus, select:focus {
            border-color: var(--border-active);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }

        .btn-predict {
            margin-top: 1.5rem;
            width: 100%;
            background: var(--brand-gradient);
            border: none;
            border-radius: 10px;
            color: #ffffff;
            font-size: 1rem;
            font-weight: 700;
            padding: 1rem;
            cursor: pointer;
            box-shadow: 0 4px 18px rgba(79, 70, 229, 0.35);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: transform 0.15s ease, filter 0.2s ease;
        }

        .btn-predict:hover {
            filter: brightness(1.1);
            transform: translateY(-1px);
        }

        .btn-predict:active {
            transform: translateY(0);
        }

        /* Analytics & Intelligence Views */
        .analytics-column {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .kpi-deck {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }

        @media (max-width: 768px) {
            .kpi-deck {
                grid-template-columns: 1fr;
            }
        }

        .kpi-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .kpi-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .kpi-val {
            font-size: 1.6rem;
            font-weight: 800;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-heading);
        }

        .badge-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            width: fit-content;
        }

        .badge-positive {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .badge-warning {
            background: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.3);
        }

        .charts-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 900px) {
            .charts-row {
                grid-template-columns: 1fr;
            }
        }

        .chart-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
        }

        .chart-container {
            position: relative;
            height: 240px;
            width: 100%;
            margin-top: 1rem;
        }

        .advisory-box {
            background: var(--bg-surface-elevated);
            border-left: 4px solid var(--brand-primary);
            border-radius: 8px;
            padding: 1rem 1.25rem;
            font-size: 0.9rem;
            color: var(--text-body);
            line-height: 1.6;
        }
    </style>
</head>
<body>

    <nav class="topbar">
        <div class="brand-container">
            <div class="brand-icon"><i class="fa-solid fa-graduation-cap"></i></div>
            <div>
                <span class="brand-title">EduPulse</span>
                <span class="brand-badge">Predictive Engine v2.0</span>
            </div>
        </div>
        <div class="system-status">
            {% if model_loaded %}
            <span class="status-dot"></span> <span>Model Loaded (RBF-SVC)</span>
            {% else %}
            <span class="status-dot offline"></span> <span>Fallback Mode (`model.pkl` missing)</span>
            {% endif %}
        </div>
    </nav>

    <div class="dashboard-wrapper">
        <!-- Input Parameters Side -->
        <div class="glass-panel">
            <div class="panel-header">
                <div>
                    <h2><i class="fa-solid fa-sliders"></i> Student Demographics & Records</h2>
                    <p>Enter normalized attributes to compute performance outlook.</p>
                </div>
            </div>

            <form id="evaluationForm">
                <div class="form-grid">
                    <div class="form-field">
                        <label>Gender</label>
                        <select name="gender">
                            <option value="0">Female</option>
                            <option value="1">Male</option>
                        </select>
                    </div>

                    <div class="form-field">
                        <label>Age</label>
                        <input type="number" name="age" value="18" min="12" max="65" required>
                    </div>

                    <div class="form-field">
                        <label>Weekly Study (Hours)</label>
                        <input type="number" step="0.1" name="study_hours" value="16.5" min="0" max="80" required>
                    </div>

                    <div class="form-field">
                        <label>Attendance Rate (%)</label>
                        <input type="number" step="0.1" name="attendance" value="88.0" min="0" max="100" required>
                    </div>

                    <div class="form-field">
                        <label>Parental Education</label>
                        <select name="parent_edu">
                            <option value="0">High School</option>
                            <option value="1" selected>Bachelor's Degree</option>
                            <option value="2">Master's Degree</option>
                            <option value="3">Doctorate</option>
                        </select>
                    </div>

                    <div class="form-field">
                        <label>Home Internet</label>
                        <select name="internet">
                            <option value="1">Available</option>
                            <option value="0">Not Available</option>
                        </select>
                    </div>

                    <div class="form-field">
                        <label>Extracurricular</label>
                        <select name="extracurricular">
                            <option value="1">Active</option>
                            <option value="0">None</option>
                        </select>
                    </div>

                    <div class="form-field">
                        <label>Previous Score (0-100)</label>
                        <input type="number" step="0.1" name="prev_score" value="74.0" min="0" max="100" required>
                    </div>

                    <div class="form-field full">
                        <label>Final / Midterm Score (0-100)</label>
                        <input type="number" step="0.1" name="final_score" value="82.5" min="0" max="100" required>
                    </div>
                </div>

                <button type="submit" class="btn-predict">
                    <i class="fa-solid fa-bolt"></i> Evaluate Student Profile
                </button>
            </form>
        </div>

        <!-- Right Side Analytics -->
        <div class="analytics-column">
            <!-- KPI Summary Cards -->
            <div class="kpi-deck">
                <div class="kpi-card">
                    <span class="kpi-label">Outcome Assessment</span>
                    <div id="outcomeBadge" class="badge-status badge-positive">
                        <i class="fa-solid fa-circle-check"></i> <span id="outcomeText">Qualified (Yes)</span>
                    </div>
                </div>

                <div class="kpi-card">
                    <span class="kpi-label">Consistency Index</span>
                    <div class="kpi-val" id="consistencyScore">86.2%</div>
                </div>

                <div class="kpi-card">
                    <span class="kpi-label">Intervention Priority</span>
                    <div class="kpi-val" id="riskLevel" style="color: #34d399; font-size: 1.3rem;">Minimal</div>
                </div>
            </div>

            <!-- Visual Analytics Grid -->
            <div class="charts-row">
                <div class="chart-card">
                    <span class="kpi-label">Holistic Competency Radar</span>
                    <div class="chart-container">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>

                <div class="chart-card">
                    <span class="kpi-label">Academic vs Cohort Benchmark</span>
                    <div class="chart-container">
                        <canvas id="barChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Prescriptive Advisory -->
            <div class="glass-panel" style="padding: 1.25rem;">
                <span class="kpi-label" style="display: block; margin-bottom: 0.5rem;">Diagnostic Insight</span>
                <div id="advisoryText" class="advisory-box">
                    Student exhibits strong classroom engagement and consistent academic retention. Continuation of current study habits is projected to maintain high outcomes.
                </div>
            </div>
        </div>
    </div>

    <script>
        // Setup Radar Chart
        const radarCtx = document.getElementById('radarChart').getContext('2d');
        const radarChart = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Study Intensity', 'Attendance', 'Prior Retention', 'Current Term', 'Socio-Edu Support'],
                datasets: [{
                    label: 'Student Profile',
                    data: [55, 88, 74, 82.5, 50],
                    backgroundColor: 'rgba(79, 70, 229, 0.25)',
                    borderColor: '#6366f1',
                    borderWidth: 2,
                    pointBackgroundColor: '#06b6d4'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
                        grid: { color: 'rgba(255, 255, 255, 0.08)' },
                        pointLabels: { color: '#94a3b8', font: { size: 10, family: 'Inter' } },
                        ticks: { display: false }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });

        // Setup Cohort Benchmark Bar Chart
        const barCtx = document.getElementById('barChart').getContext('2d');
        const barChart = new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: ['Prev Score', 'Final Score', 'Attendance'],
                datasets: [
                    {
                        label: 'Student',
                        data: [74.0, 82.5, 88.0],
                        backgroundColor: '#4f46e5',
                        borderRadius: 6
                    },
                    {
                        label: 'Median Cohort',
                        data: [65.0, 68.0, 75.0],
                        backgroundColor: 'rgba(255, 255, 255, 0.15)',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
                    y: { max: 100, grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
                },
                plugins: {
                    legend: { labels: { color: '#cbd5e1', font: { size: 11 } } }
                }
            }
        });

        // Form Submit Handler
        document.getElementById('evaluationForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                const res = await response.json();

                if (res.status !== 'success') return;

                const isQualified = res.prediction.toLowerCase() === 'yes';
                const badge = document.getElementById('outcomeBadge');
                const outcomeText = document.getElementById('outcomeText');
                const riskLevel = document.getElementById('riskLevel');
                const advisoryText = document.getElementById('advisoryText');
                const consistencyScore = document.getElementById('consistencyScore');

                if (isQualified) {
                    badge.className = 'badge-status badge-positive';
                    outcomeText.innerHTML = 'Positive (Pass/Qualified)';
                    riskLevel.innerText = 'Low Priority';
                    riskLevel.style.color = '#34d399';
                    advisoryText.innerText = 'Student parameters fall within standard passing bounds. Maintain study cadence and weekly assignments.';
                } else {
                    badge.className = 'badge-status badge-warning';
                    outcomeText.innerHTML = 'At Risk (Unqualified/Fail)';
                    riskLevel.innerText = 'High Priority';
                    riskLevel.style.color = '#fb7185';
                    advisoryText.innerText = 'Alert: Low study intensity or low attendance observed. Recommended intervention: peer tutoring and attendance follow-ups.';
                }

                // Consistency Index Calculation
                const avgScore = ((res.features.prev_score + res.features.final_score + res.features.attendance) / 3).toFixed(1);
                consistencyScore.innerText = `${avgScore}%`;

                // Update Charts
                const studyNorm = Math.min((res.features.study_hours / 30) * 100, 100);
                radarChart.data.datasets[0].data = [
                    studyNorm,
                    res.features.attendance,
                    res.features.prev_score,
                    res.features.final_score,
                    (res.features.parent_edu / 3) * 100
                ];
                radarChart.update();

                barChart.data.datasets[0].data = [
                    res.features.prev_score,
                    res.features.final_score,
                    res.features.attendance
                ];
                barChart.update();

            } catch (err) {
                console.error("Inference Error:", err);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, model_loaded=(model is not None))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features matching the model's exact signature:
        # ['gender', 'age', 'study_hours_per_week', 'attendance_rate', 'parent_education', 'internet_access', 'extracurricular', 'previous_score', 'final_score']
        gender = float(request.form.get('gender', 0))
        age = float(request.form.get('age', 18))
        study_hours = float(request.form.get('study_hours', 10.0))
        attendance = float(request.form.get('attendance', 75.0))
        parent_edu = float(request.form.get('parent_edu', 1))
        internet = float(request.form.get('internet', 1))
        extracurricular = float(request.form.get('extracurricular', 0))
        prev_score = float(request.form.get('prev_score', 60.0))
        final_score = float(request.form.get('final_score', 65.0))

        features = np.array([[gender, age, study_hours, attendance, parent_edu, internet, extracurricular, prev_score, final_score]])

        if model:
            pred = model.predict(features)[0]
        else:
            # Fallback heuristic if running without pickle in testing environment
            pred = "Yes" if (attendance >= 70 and final_score >= 50) else "No"

        return jsonify({
            'status': 'success',
            'prediction': str(pred),
            'features': {
                'study_hours': study_hours,
                'attendance': attendance,
                'parent_edu': parent_edu,
                'prev_score': prev_score,
                'final_score': final_score
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
