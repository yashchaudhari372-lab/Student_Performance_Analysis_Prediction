import os
import pickle
import numpy as np
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Dynamically resolve relative file path for local and serverless execution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')

model = None
if os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"Model load error: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="indigo">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Performance Analysis Prediction</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        /* Multi-Theme Palette Configurations */
        :root[data-theme="indigo"] {
            --bg-base: #0b0f19;
            --bg-card: rgba(18, 24, 38, 0.85);
            --bg-input: #111827;
            --border-card: rgba(99, 102, 241, 0.2);
            --border-input: rgba(255, 255, 255, 0.08);
            --accent-primary: #6366f1;
            --accent-secondary: #06b6d4;
            --accent-gradient: linear-gradient(135deg, #6366f1, #06b6d4);
            --glow: 0 10px 30px -10px rgba(99, 102, 241, 0.4);
            --text-heading: #f9fafb;
            --text-body: #9ca3af;
        }

        :root[data-theme="emerald"] {
            --bg-base: #061412;
            --bg-card: rgba(10, 30, 26, 0.85);
            --bg-input: #08211d;
            --border-card: rgba(16, 185, 129, 0.2);
            --border-input: rgba(255, 255, 255, 0.08);
            --accent-primary: #10b981;
            --accent-secondary: #14b8a6;
            --accent-gradient: linear-gradient(135deg, #10b981, #14b8a6);
            --glow: 0 10px 30px -10px rgba(16, 185, 129, 0.4);
            --text-heading: #ecfdf5;
            --text-body: #a7f3d0;
        }

        :root[data-theme="crimson"] {
            --bg-base: #14080e;
            --bg-card: rgba(31, 14, 23, 0.85);
            --bg-input: #230d19;
            --border-card: rgba(244, 63, 94, 0.2);
            --border-input: rgba(255, 255, 255, 0.08);
            --accent-primary: #f43f5e;
            --accent-secondary: #fb7185;
            --accent-gradient: linear-gradient(135deg, #f43f5e, #fb7185);
            --glow: 0 10px 30px -10px rgba(244, 63, 94, 0.4);
            --text-heading: #fff1f2;
            --text-body: #fecdd3;
        }

        :root[data-theme="amber"] {
            --bg-base: #140d05;
            --bg-card: rgba(33, 21, 10, 0.85);
            --bg-input: #271707;
            --border-card: rgba(245, 158, 11, 0.2);
            --border-input: rgba(255, 255, 255, 0.08);
            --accent-primary: #f59e0b;
            --accent-secondary: #d97706;
            --accent-gradient: linear-gradient(135deg, #f59e0b, #d97706);
            --glow: 0 10px 30px -10px rgba(245, 158, 11, 0.4);
            --text-heading: #fffbeb;
            --text-body: #fde68a;
        }

        :root[data-theme="cyber"] {
            --bg-base: #0c0814;
            --bg-card: rgba(25, 16, 42, 0.85);
            --bg-input: #190f2b;
            --border-card: rgba(217, 70, 239, 0.2);
            --border-input: rgba(255, 255, 255, 0.08);
            --accent-primary: #d946ef;
            --accent-secondary: #8b5cf6;
            --accent-gradient: linear-gradient(135deg, #d946ef, #8b5cf6);
            --glow: 0 10px 30px -10px rgba(217, 70, 239, 0.4);
            --text-heading: #fdf4ff;
            --text-body: #e879f9;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: background-color 0.25s ease, border-color 0.25s ease, color 0.25s ease;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-base);
            color: var(--text-heading);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Top Header */
        header {
            padding: 1.1rem 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(11, 15, 25, 0.7);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-card);
            position: sticky;
            top: 0;
            z-index: 40;
        }

        .brand-meta {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-badge {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: var(--accent-gradient);
            display: grid;
            place-items: center;
            font-size: 1.15rem;
            color: #ffffff;
            box-shadow: var(--glow);
        }

        .brand-title {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .theme-strip {
            display: flex;
            align-items: center;
            gap: 10px;
            background: var(--bg-input);
            padding: 6px 12px;
            border-radius: 9999px;
            border: 1px solid var(--border-card);
        }

        .theme-strip span {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-body);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-right: 4px;
        }

        .swatch-btn {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            border: 2px solid transparent;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .swatch-btn:hover { transform: scale(1.2); }
        .swatch-btn.active { border-color: #ffffff; transform: scale(1.1); }

        .swatch-indigo { background: linear-gradient(135deg, #6366f1, #06b6d4); }
        .swatch-emerald { background: linear-gradient(135deg, #10b981, #14b8a6); }
        .swatch-crimson { background: linear-gradient(135deg, #f43f5e, #fb7185); }
        .swatch-amber { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .swatch-cyber { background: linear-gradient(135deg, #d946ef, #8b5cf6); }

        /* Container Layout */
        .workspace {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 1.5rem;
            width: 100%;
            display: grid;
            grid-template-columns: 460px 1fr;
            gap: 2rem;
            flex: 1;
        }

        @media (max-width: 1024px) {
            .workspace { grid-template-columns: 1fr; }
        }

        /* Glass Panel Styling */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 20px;
            padding: 1.75rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-input);
            padding-bottom: 1rem;
        }

        .card-title {
            font-size: 1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-title i {
            color: var(--accent-primary);
        }

        /* Input Controls */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .input-group.full-width {
            grid-column: span 2;
        }

        label {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-body);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .input-field {
            background: var(--bg-input);
            border: 1px solid var(--border-input);
            border-radius: 12px;
            padding: 0.75rem 0.9rem;
            color: var(--text-heading);
            font-family: inherit;
            font-size: 0.9rem;
            outline: none;
        }

        .input-field:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }

        .btn-predict {
            margin-top: 0.5rem;
            padding: 1rem;
            border: none;
            border-radius: 12px;
            background: var(--accent-gradient);
            color: #ffffff;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: var(--glow);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .btn-predict:hover {
            filter: brightness(1.1);
            transform: translateY(-2px);
        }

        /* Analytics & Output Prediction Display */
        .analytics-deck {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .prediction-hero-card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 20px;
            padding: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        .prediction-hero-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 6px;
            background: var(--accent-gradient);
        }

        .prediction-hero-title {
            font-size: 0.8rem;
            color: var(--text-body);
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
        }

        .prediction-subtext {
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 4px;
        }

        /* Strict YES / NO Badge Outputs */
        .result-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.2rem;
            font-weight: 800;
            padding: 0.4rem 2.2rem;
            border-radius: 16px;
            letter-spacing: 1.5px;
            text-align: center;
        }

        .result-initial {
            background: rgba(148, 163, 184, 0.15);
            color: #94a3b8;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }

        .result-yes {
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
            border: 2px solid #10b981;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.3);
        }

        .result-no {
            background: rgba(244, 63, 94, 0.15);
            color: #f43f5e;
            border: 2px solid #f43f5e;
            box-shadow: 0 0 25px rgba(244, 63, 94, 0.3);
        }

        /* Charts Container */
        .charts-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 800px) {
            .charts-row { grid-template-columns: 1fr; }
        }

        .chart-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 20px;
            padding: 1.5rem;
            height: 310px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .chart-box {
            position: relative;
            flex: 1;
            width: 100%;
        }
    </style>
</head>
<body>

    <header>
        <div class="brand-meta">
            <div class="brand-badge">
                <i class="fa-solid fa-chart-pie"></i>
            </div>
            <div class="brand-title">Student Performance Analysis Prediction</div>
        </div>

        <div class="theme-strip">
            <span>Themes</span>
            <div class="swatch-btn swatch-indigo active" data-t="indigo" title="Indigo Modern"></div>
            <div class="swatch-btn swatch-emerald" data-t="emerald" title="Emerald Matrix"></div>
            <div class="swatch-btn swatch-crimson" data-t="crimson" title="Crimson Ember"></div>
            <div class="swatch-btn swatch-amber" data-t="amber" title="Amber Dusk"></div>
            <div class="swatch-btn swatch-cyber" data-t="cyber" title="Cyber Violet"></div>
        </div>
    </header>

    <main class="workspace">
        <!-- Input Parameters Section -->
        <section class="card">
            <div class="card-header">
                <div class="card-title">
                    <i class="fa-solid fa-sliders"></i>
                    <span>Student Profile Inputs</span>
                </div>
                <span style="font-size: 0.75rem; color: var(--text-body); font-family: 'JetBrains Mono', monospace;">9 FEATURES</span>
            </div>

            <form id="predictForm">
                <div class="form-grid">
                    <div class="input-group">
                        <label>Gender</label>
                        <select name="gender" class="input-field">
                            <option value="0">Female</option>
                            <option value="1">Male</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Age</label>
                        <input type="number" name="age" class="input-field" value="18" min="10" max="80" required>
                    </div>

                    <div class="input-group">
                        <label>Study Hours / Week</label>
                        <input type="number" step="0.1" name="study_hours" class="input-field" value="16.5" required>
                    </div>

                    <div class="input-group">
                        <label>Attendance Rate (%)</label>
                        <input type="number" step="0.1" name="attendance" class="input-field" value="86.0" min="0" max="100" required>
                    </div>

                    <div class="input-group">
                        <label>Parent Education</label>
                        <select name="parent_edu" class="input-field">
                            <option value="0">High School</option>
                            <option value="1" selected>Bachelor's</option>
                            <option value="2">Master's</option>
                            <option value="3">Doctorate</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Internet Access</label>
                        <select name="internet" class="input-field">
                            <option value="1" selected>Yes</option>
                            <option value="0">No</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Extracurricular</label>
                        <select name="extracurricular" class="input-field">
                            <option value="1" selected>Yes</option>
                            <option value="0">No</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Previous Score</label>
                        <input type="number" step="0.1" name="prev_score" class="input-field" value="72.0" min="0" max="100" required>
                    </div>

                    <div class="input-group full-width">
                        <label>Final / Midterm Score</label>
                        <input type="number" step="0.1" name="final_score" class="input-field" value="79.5" min="0" max="100" required>
                    </div>
                </div>

                <button type="submit" class="btn-predict full-width" style="width: 100%; margin-top: 1.25rem;">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Run Analysis & Predict
                </button>
            </form>
        </section>

        <!-- Prediction Output Display -->
        <section class="analytics-deck">
            <div class="prediction-hero-card">
                <div>
                    <div class="prediction-hero-title">Output Prediction</div>
                    <div class="prediction-subtext">Student Result</div>
                </div>
                <div id="outputResultBadge" class="result-badge result-initial">--</div>
            </div>

            <!-- Charts Dynamic Rendering -->
            <div class="charts-row">
                <div class="chart-panel">
                    <span style="font-size: 0.75rem; color: var(--text-body); font-weight: 700; text-transform: uppercase;">Feature Metric Distribution</span>
                    <div class="chart-box">
                        <canvas id="radarDistChart"></canvas>
                    </div>
                </div>

                <div class="chart-panel">
                    <span style="font-size: 0.75rem; color: var(--text-body); font-weight: 700; text-transform: uppercase;">Academic Progression</span>
                    <div class="chart-box">
                        <canvas id="progressionBarChart"></canvas>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        // Multi-Theme Switching System
        const swatchBtns = document.querySelectorAll('.swatch-btn');
        swatchBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                swatchBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const selectedTheme = btn.getAttribute('data-t');
                document.documentElement.setAttribute('data-theme', selectedTheme);
                refreshVisualTheme();
            });
        });

        // Initialize Radar Chart
        const ctxRadar = document.getElementById('radarDistChart').getContext('2d');
        const radarDistChart = new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ['Study Hours', 'Attendance', 'Prev Score', 'Final Score', 'Parent Edu'],
                datasets: [{
                    label: 'Current Attributes',
                    data: [55, 86, 72, 79.5, 33],
                    backgroundColor: 'rgba(99, 102, 241, 0.2)',
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
                        grid: { color: 'rgba(255, 255, 255, 0.08)' },
                        angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
                        pointLabels: { color: '#9ca3af', font: { family: 'Plus Jakarta Sans', size: 10 } },
                        ticks: { display: false }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });

        // Initialize Progression Bar Chart
        const ctxBar = document.getElementById('progressionBarChart').getContext('2d');
        const progressionBarChart = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['Previous Score', 'Final Score', 'Study Hours'],
                datasets: [{
                    data: [72.0, 79.5, 16.5],
                    backgroundColor: ['rgba(156, 163, 175, 0.35)', '#6366f1', '#06b6d4'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#9ca3af' } },
                    x: { grid: { display: false }, ticks: { color: '#9ca3af' } }
                },
                plugins: { legend: { display: false } }
            }
        });

        function refreshVisualTheme() {
            const rootStyle = getComputedStyle(document.documentElement);
            const primary = rootStyle.getPropertyValue('--accent-primary').trim();
            const secondary = rootStyle.getPropertyValue('--accent-secondary').trim();

            radarDistChart.data.datasets[0].borderColor = primary;
            radarDistChart.data.datasets[0].pointBackgroundColor = secondary;
            radarDistChart.data.datasets[0].backgroundColor = primary + '33';
            radarDistChart.update();

            progressionBarChart.data.datasets[0].backgroundColor[1] = primary;
            progressionBarChart.data.datasets[0].backgroundColor[2] = secondary;
            progressionBarChart.update();
        }

        // Form Submit Handler & Prediction Extraction
        document.getElementById('predictForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);

            try {
                const res = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                const payload = await res.json();

                if (payload.status === 'success') {
                    const badge = document.getElementById('outputResultBadge');
                    const cleanResult = payload.prediction.trim().toUpperCase();

                    badge.innerText = cleanResult;

                    if (cleanResult === 'YES') {
                        badge.className = 'result-badge result-yes';
                    } else {
                        badge.className = 'result-badge result-no';
                    }

                    // Dynamically refresh charts
                    const studyNormalized = Math.min((payload.features.study_hours / 30) * 100, 100);
                    radarDistChart.data.datasets[0].data = [
                        studyNormalized,
                        payload.features.attendance,
                        payload.features.prev_score,
                        payload.features.final_score,
                        (payload.features.parent_edu / 3) * 100
                    ];
                    radarDistChart.update();

                    progressionBarChart.data.datasets[0].data = [
                        payload.features.prev_score,
                        payload.features.final_score,
                        payload.features.study_hours
                    ];
                    progressionBarChart.update();
                }
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
    return render_template_string(HTML_TEMPLATE)

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
            # Normalize model output strictly to "Yes" or "No"
            prediction = "Yes" if str(raw_pred).strip().lower() in ['yes', '1', '1.0', 'true'] else "No"
        else:
            # Standalone fallback calculation
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

# Vercel entry point
app_handler = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
