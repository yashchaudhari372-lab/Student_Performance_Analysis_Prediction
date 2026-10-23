import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Resolve model path dynamically for both local runs and Vercel serverless environments
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')

model = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"Error loading model: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduPulse AI | Predictive Student Intelligence Engine</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {
            --bg-base: #090d16;
            --bg-surface: #0f172a;
            --bg-elevated: #162036;
            --border: rgba(148, 163, 184, 0.12);
            --border-highlight: rgba(99, 102, 241, 0.3);
            --primary: #4f46e5;
            --primary-glow: rgba(79, 70, 229, 0.25);
            --cyan: #06b6d4;
            --emerald: #10b981;
            --rose: #f43f5e;
            --amber: #f59e0b;
            --text-heading: #f8fafc;
            --text-body: #94a3b8;
            --text-muted: #64748b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-base);
            color: var(--text-heading);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            background-image: 
                radial-gradient(ellipse at 15% 10%, rgba(79, 70, 229, 0.12) 0%, transparent 45%),
                radial-gradient(ellipse at 85% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 40%);
            background-attachment: fixed;
        }

        /* Top Navigation */
        .navbar {
            height: 72px;
            border-bottom: 1px solid var(--border);
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(20px);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2.5rem;
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .brand-container {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .brand-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, #4f46e5, #06b6d4);
            display: grid;
            place-items: center;
            font-size: 1.25rem;
            color: #fff;
            box-shadow: 0 8px 16px var(--primary-glow);
        }

        .brand-text h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .brand-text p {
            font-size: 0.72rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
        }

        .system-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            padding: 6px 14px;
            border-radius: 9999px;
            border: 1px solid var(--border);
            background: var(--bg-surface);
        }

        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--emerald);
            box-shadow: 0 0 10px var(--emerald);
        }

        .status-dot.offline {
            background: var(--amber);
            box-shadow: 0 0 10px var(--amber);
        }

        /* Main Workspace */
        .workspace {
            max-width: 1440px;
            margin: 2rem auto;
            padding: 0 2rem;
            width: 100%;
            display: grid;
            grid-template-columns: 460px 1fr;
            gap: 2rem;
            flex: 1;
        }

        @media (max-width: 1100px) {
            .workspace { grid-template-columns: 1fr; }
        }

        /* Glass Cards */
        .panel {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .panel-header {
            padding: 1.25rem 1.75rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.01);
        }

        .panel-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            letter-spacing: -0.01em;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .panel-body {
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        /* Form Inputs */
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .input-group label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-body);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .input-field {
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.75rem 0.9rem;
            font-size: 0.9rem;
            font-family: inherit;
            color: var(--text-heading);
            outline: none;
            transition: all 0.2s;
        }

        .input-field:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        .submit-action {
            margin-top: 0.5rem;
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 0.95rem;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            color: #fff;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            box-shadow: 0 8px 24px var(--primary-glow);
            transition: all 0.2s ease;
        }

        .submit-action:hover {
            transform: translateY(-2px);
            filter: brightness(1.1);
        }

        /* Analytics Workspace */
        .analytics-grid {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .kpi-deck {
            display: grid;
            grid-template-columns: 1.2fr 1fr 1fr;
            gap: 1rem;
        }

        @media (max-width: 768px) {
            .kpi-deck { grid-template-columns: 1fr; }
        }

        .kpi-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }

        .kpi-card.hero {
            background: linear-gradient(145deg, rgba(79, 70, 229, 0.15), rgba(15, 23, 42, 0.8));
            border-color: var(--border-highlight);
        }

        .kpi-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
        }

        .kpi-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.9rem;
            font-weight: 700;
            margin-top: 0.35rem;
            display: flex;
            align-items: baseline;
            gap: 8px;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }

        .badge-success { background: rgba(16, 185, 129, 0.15); color: var(--emerald); border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-danger { background: rgba(244, 63, 94, 0.15); color: var(--rose); border: 1px solid rgba(244, 63, 94, 0.3); }

        .charts-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 900px) {
            .charts-row { grid-template-columns: 1fr; }
        }

        .chart-box {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            height: 320px;
        }

        .chart-wrapper {
            position: relative;
            flex: 1;
            width: 100%;
        }

        /* Recommendation Section */
        .rec-box {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }

        .rec-icon {
            width: 44px;
            height: 44px;
            border-radius: 10px;
            background: rgba(6, 182, 212, 0.15);
            color: var(--cyan);
            display: grid;
            place-items: center;
            font-size: 1.2rem;
            flex-shrink: 0;
        }

        .rec-text h4 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
        }

        .rec-text p {
            font-size: 0.85rem;
            color: var(--text-body);
            margin-top: 2px;
        }
    </style>
</head>
<body>

    <nav class="navbar">
        <div class="brand-container">
            <div class="brand-icon">
                <i class="fa-solid fa-graduation-cap"></i>
            </div>
            <div class="brand-text">
                <h1>EduPulse AI</h1>
                <p>Enterprise Student Performance Intelligence</p>
            </div>
        </div>

        <div class="system-pill">
            {% if model_loaded %}
            <span class="status-dot"></span>
            <span>RBF-SVC ENGINE READY</span>
            {% else %}
            <span class="status-dot offline"></span>
            <span>HEURISTIC SIMULATION MODE</span>
            {% endif %}
        </div>
    </nav>

    <main class="workspace">
        <!-- Input Parameters Section -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    <i class="fa-solid fa-sliders" style="color: var(--cyan)"></i>
                    <span>Candidate Profile & Metrics</span>
                </div>
                <span style="font-size: 0.75rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">9 FEATURES</span>
            </div>

            <form id="evaluationForm" class="panel-body">
                <div class="form-row">
                    <div class="input-group">
                        <label>Gender</label>
                        <select name="gender" class="input-field">
                            <option value="0">Female</option>
                            <option value="1">Male</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label>Age</label>
                        <input type="number" name="age" class="input-field" value="18" min="12" max="60" required>
                    </div>
                </div>

                <div class="form-row">
                    <div class="input-group">
                        <label>Weekly Study (Hours)</label>
                        <input type="number" step="0.5" name="study_hours" class="input-field" value="16.0" required>
                    </div>
                    <div class="input-group">
                        <label>Attendance Rate (%)</label>
                        <input type="number" step="0.5" name="attendance" class="input-field" value="88.0" min="0" max="100" required>
                    </div>
                </div>

                <div class="form-row">
                    <div class="input-group">
                        <label>Parental Education</label>
                        <select name="parent_edu" class="input-field">
                            <option value="0">High School</option>
                            <option value="1" selected>Bachelor's Degree</option>
                            <option value="2">Master's Degree</option>
                            <option value="3">Doctorate (PhD)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label>Internet Access</label>
                        <select name="internet" class="input-field">
                            <option value="1" selected>Available</option>
                            <option value="0">Unavailable</option>
                        </select>
                    </div>
                </div>

                <div class="input-group">
                    <label>Extracurricular Participation</label>
                    <select name="extracurricular" class="input-field">
                        <option value="1" selected>Active Member</option>
                        <option value="0">None</option>
                    </select>
                </div>

                <div class="form-row">
                    <div class="input-group">
                        <label>Previous Term Score</label>
                        <input type="number" step="0.1" name="prev_score" class="input-field" value="74.0" min="0" max="100" required>
                    </div>
                    <div class="input-group">
                        <label>Current / Midterm Score</label>
                        <input type="number" step="0.1" name="final_score" class="input-field" value="80.5" min="0" max="100" required>
                    </div>
                </div>

                <button type="submit" class="submit-action">
                    <i class="fa-solid fa-bolt"></i> Evaluate Performance Prognosis
                </button>
            </form>
        </section>

        <!-- Dynamic Output & Intelligence Deck -->
        <section class="analytics-grid">
            <!-- Top KPI Deck -->
            <div class="kpi-deck">
                <div class="kpi-card hero">
                    <span class="kpi-label">Outcome Prediction</span>
                    <div class="kpi-value">
                        <span id="badgeOutcome" class="status-badge badge-success">INITIALIZED</span>
                    </div>
                    <span id="decisionLabel" style="font-size: 0.78rem; color: var(--text-body); margin-top: 4px;">Ready to run inference</span>
                </div>

                <div class="kpi-card">
                    <span class="kpi-label">Academic Momentum</span>
                    <div class="kpi-value">
                        <span id="deltaScore">+6.5</span>
                        <span style="font-size: 0.85rem; color: var(--emerald); font-weight: 500;"><i class="fa-solid fa-arrow-trend-up"></i> pts</span>
                    </div>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">Current vs Previous</span>
                </div>

                <div class="kpi-card">
                    <span class="kpi-label">Engagement Quotient</span>
                    <div class="kpi-value">
                        <span id="engagementIdx">88%</span>
                    </div>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">Attendance & Extracurricular</span>
                </div>
            </div>

            <!-- Visualization Row -->
            <div class="charts-row">
                <div class="chart-box">
                    <span class="kpi-label">Feature Vector Distribution</span>
                    <div class="chart-wrapper">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>

                <div class="chart-box">
                    <span class="kpi-label">Trajectory Comparison</span>
                    <div class="chart-wrapper">
                        <canvas id="barChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Strategic Action Advisory -->
            <div class="rec-box">
                <div class="rec-icon">
                    <i class="fa-solid fa-compass"></i>
                </div>
                <div class="rec-text">
                    <h4 id="advisoryTitle">Predictive Prognosis Standing By</h4>
                    <p id="advisoryBody">Submit student attributes on the left to evaluate performance likelihood and generate proactive interventions.</p>
                </div>
            </div>
        </section>
    </main>

    <script>
        // Radar Chart Initialization
        const ctxRadar = document.getElementById('radarChart').getContext('2d');
        const radarChart = new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ['Study Intensity', 'Attendance', 'Pre-Score', 'Current Score', 'Environment'],
                datasets: [{
                    label: 'Normalized Attributes',
                    data: [55, 88, 74, 80.5, 75],
                    backgroundColor: 'rgba(79, 70, 229, 0.25)',
                    borderColor: '#6366f1',
                    pointBackgroundColor: '#06b6d4',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        grid: { color: 'rgba(148, 163, 184, 0.1)' },
                        angleLines: { color: 'rgba(148, 163, 184, 0.15)' },
                        pointLabels: { color: '#94a3b8', font: { family: 'Inter', size: 10 } },
                        ticks: { display: false }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });

        // Bar Trajectory Initialization
        const ctxBar = document.getElementById('barChart').getContext('2d');
        const barChart = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['Previous Score', 'Midterm Score', 'Weekly Study Hours'],
                datasets: [{
                    data: [74.0, 80.5, 16.0],
                    backgroundColor: ['rgba(148, 163, 184, 0.3)', '#4f46e5', '#06b6d4'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: 'rgba(148, 163, 184, 0.08)' }, ticks: { color: '#64748b' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                },
                plugins: { legend: { display: false } }
            }
        });

        // Async Form Submission
        document.getElementById('evaluationForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);

            try {
                const res = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();

                if (data.status === 'success') {
                    const isPositive = data.prediction.toLowerCase() === 'yes';
                    const badge = document.getElementById('badgeOutcome');
                    const decision = document.getElementById('decisionLabel');
                    const advTitle = document.getElementById('advisoryTitle');
                    const advBody = document.getElementById('advisoryBody');

                    if (isPositive) {
                        badge.className = 'status-badge badge-success';
                        badge.innerHTML = '<i class="fa-solid fa-circle-check"></i> PASS PROSPECT';
                        decision.innerText = 'High probability of passing target';
                        advTitle.innerText = 'High Academic Stability Detected';
                        advBody.innerText = 'Student demonstrates strong metric consistency. Retain study regimen and encourage leadership in extracurricular activities.';
                    } else {
                        badge.className = 'status-badge badge-danger';
                        badge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> RISK DETECTED';
                        decision.innerText = 'At risk of academic underperformance';
                        advTitle.innerText = 'Targeted Intervention Advised';
                        advBody.innerText = 'Current attendance and score trends suggest intervention is needed. Prioritize mandatory tutoring and weekly review checkpoints.';
                    }

                    // Delta computation
                    const diff = (data.features.final_score - data.features.prev_score).toFixed(1);
                    const deltaEl = document.getElementById('deltaScore');
                    deltaEl.innerText = (diff >= 0 ? '+' : '') + diff;

                    // Engagement computation
                    document.getElementById('engagementIdx').innerText = Math.round(data.features.attendance) + '%';

                    // Update Charts
                    const studyNorm = Math.min((data.features.study_hours / 30) * 100, 100);
                    const envNorm = ((data.features.parent_edu / 3) * 50) + (data.features.internet * 50);

                    radarChart.data.datasets[0].data = [
                        studyNorm,
                        data.features.attendance,
                        data.features.prev_score,
                        data.features.final_score,
                        envNorm
                    ];
                    radarChart.update();

                    barChart.data.datasets[0].data = [
                        data.features.prev_score,
                        data.features.final_score,
                        data.features.study_hours
                    ];
                    barChart.update();
                }
            } catch (err) {
                console.error("Prediction error:", err);
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
        gender = float(request.form.get('gender', 0))
        age = float(request.form.get('age', 18))
        study_hours = float(request.form.get('study_hours', 0))
        attendance = float(request.form.get('attendance', 0))
        parent_edu = float(request.form.get('parent_edu', 0))
        internet = float(request.form.get('internet', 0))
        extracurricular = float(request.form.get('extracurricular', 0))
        prev_score = float(request.form.get('prev_score', 0))
        final_score = float(request.form.get('final_score', 0))

        # Vector aligns with: ['gender', 'age', 'study_hours_per_week', 'attendance_rate', 
        #                      'parent_education', 'internet_access', 'extracurricular', 
        #                      'previous_score', 'final_score']
        features = np.array([[gender, age, study_hours, attendance, parent_edu, internet, extracurricular, prev_score, final_score]])

        if model is not None:
            raw_pred = model.predict(features)[0]
            prediction = str(raw_pred)
        else:
            # Fallback heuristic if model file isn't found in current directory
            prediction = "Yes" if (attendance >= 75 and (final_score + prev_score) / 2 >= 60) else "No"

        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'features': {
                'gender': gender,
                'age': age,
                'study_hours': study_hours,
                'attendance': attendance,
                'parent_edu': parent_edu,
                'internet': internet,
                'extracurricular': extracurricular,
                'prev_score': prev_score,
                'final_score': final_score
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Vercel WSGI entry point
app_handler = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
