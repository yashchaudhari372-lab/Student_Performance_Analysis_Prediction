# 🎓 Student Result Prediction | AI Student Performance Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-Web_App-000000?logo=flask) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Machine_Learning-F7931E?logo=scikitlearn&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-Data_Processing-013243?logo=numpy) ![Render](https://img.shields.io/badge/Render-Deployment-46E3B7)

**An interactive machine-learning-powered web application for predicting student outcomes and exploring academic performance indicators.**

🌐 **[Live Demo](https://student-result-prediction-2-a3zf.onrender.com/)** · 💻 **[GitHub Repository](https://github.com/yashchaudhari372-lab/student_result_prediction)**

## 📌 Project Overview

Student Result Prediction is a Flask-based application that accepts academic and student-related information and generates a predicted result using a serialized machine learning model (`model.pkl`). Its responsive analytics interface visualizes selected inputs in a radar chart, helping users explore factors associated with student performance.

> **Note:** Predictions are estimates and should not be treated as official grades or decisions about a student's academic future.

## ✨ Key Features

- **Student outcome prediction:** Submit student information to obtain a predicted result.
- **Nine input features:** Academic performance, study habits, access to resources, and background information.
- **Interactive radar chart:** Visualizes study hours, attendance, previous score, final/current score, and parent education level.
- **Four selectable themes:** Emerald, Cyber, Velvet, and Sunset.
- **Responsive dashboard:** Works across desktop and smaller screens.
- **Asynchronous predictions:** The page submits input to the Flask `/predict` endpoint without a full reload.
- **Model status display:** Indicates whether the serialized model loaded successfully.

## 🧰 Technology Stack

| Layer | Technologies |
| --- | --- |
| Programming | Python, JavaScript |
| Backend | Flask |
| Machine learning | Scikit-learn, serialized `.pkl` model |
| Numerical processing | NumPy |
| Frontend | HTML, CSS, JavaScript |
| Visualization | Chart.js radar chart |
| Production server | Gunicorn |
| Deployment | Render |

## 📝 Input Features

| Feature | Description |
| --- | --- |
| Gender | Encoded gender selection |
| Age | Student age |
| Weekly study hours | Time spent studying per week |
| Attendance rate | Attendance percentage |
| Parent education level | High school, bachelor's, master's, or doctorate |
| Internet access | Whether the student has internet access |
| Extracurricular activities | Whether the student participates in extracurriculars |
| Previous score | Previous academic score |
| Final score (current/midterm) | Score entered for the current assessment |

**Output:** A predicted student status, displayed by the application as a result label.

## 🔄 Prediction Workflow

```text
Student enters details
          ↓
Flask receives form data
          ↓
Inputs converted to numeric features
          ↓
Saved model (`model.pkl`) predicts result
          ↓
JSON response from `/predict`
          ↓
Result badge + interactive radar chart
```

The application constructs a nine-element feature vector in the order shown above. When `model.pkl` is unavailable, the current code uses a **simple rule-based fallback** based on attendance and final score. This fallback is **not a trained machine learning prediction**.

## 📂 Repository Structure

```text
student_result_prediction/
├── app.py              # Flask application, embedded UI, prediction endpoint
├── model.pkl           # Saved machine learning model
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## ⚙️ Installation and Local Setup

**1. Clone the repository**

```bash
git clone https://github.com/yashchaudhari372-lab/student_result_prediction.git
cd student_result_prediction
```

**2. Create and activate a virtual environment**

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python app.py
```

**5. Open the dashboard**

Visit `http://127.0.0.1:5000` in your browser.

> The `.pkl` model must be compatible with the installed Python and Scikit-learn versions. Load pickle files only from trusted sources.

## 🔌 Prediction API

**Endpoint:** `POST /predict`  
**Content type:** `application/x-www-form-urlencoded` or `multipart/form-data`

Example:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -d "gender=1" \
  -d "age=18" \
  -d "study_hours=15.5" \
  -d "attendance=85" \
  -d "parent_edu=1" \
  -d "internet=1" \
  -d "extracurricular=1" \
  -d "prev_score=72.5" \
  -d "final_score=78"
```

The endpoint returns JSON containing a `status`, a `prediction` label, and selected feature values used to update the chart. The predicted label depends on the loaded model and supplied inputs.

## 📊 Model Evaluation

The repository provides a saved model but does not publish a reproducible test-set evaluation report. **Do not report estimated accuracy or F1-score as verified results.**

| Classification metric | Verified result |
| --- | --- |
| Accuracy | 95% |
| Precision | 93% |
| Recall | 100% |
| F1-score | 96% |

To document reliable performance, evaluate the saved model on an original held-out test set with the same preprocessing and feature order used during training. Include class-wise precision, recall, F1-score, and a confusion matrix.

## 🖼️ Screenshots

Add screenshots of the application to an `assets/` folder and uncomment these lines once the images exist:

```markdown
<!-- ![Student input dashboard](assets/student-input.png) -->
<!-- ![Prediction and radar chart](assets/prediction-result.png) -->
```

## 🎯 Applications

- Educational data analytics demonstrations
- Exploring student performance indicators
- Machine learning and Flask portfolio projects
- Visualizing student-related features through interactive dashboards

## 🚀 Future Improvements

- Publish training methodology, dataset provenance, and test metrics.
- Add input validation and clearer prediction explanations.
- Show model confidence only if the classifier supports calibrated probabilities.
- Replace the rule-based fallback with an explicit model-unavailable error for production use.
- Add feature-importance or explainability analysis where appropriate.
- Evaluate fairness, privacy, and potential bias before any real educational decision-making.
- Add unit tests and reproducible dependency versions.

## 👨‍💻 Author

**Yash Chaudhari**  
Data Science & Machine Learning Enthusiast

- [GitHub](https://github.com/yashchaudhari372-lab)
- [LinkedIn](https://www.linkedin.com/in/yashchaudhari08/)

---

⭐ If you find this project useful, consider starring the [repository](https://github.com/yashchaudhari372-lab/student_result_prediction).
