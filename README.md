# 🎓 Student Performance Analysis and Prediction | AI-Powered Academic Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-Web_App-000000?logo=flask&logoColor=white) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Machine_Learning-F7931E?logo=scikitlearn&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-Data_Processing-013243?logo=numpy&logoColor=white) ![Vercel](https://img.shields.io/badge/Vercel-Deployment-000000?logo=vercel&logoColor=white)

**An interactive machine-learning-powered web application for analyzing student-related factors and predicting academic outcomes through an intuitive and responsive dashboard.**

🌐 **[Live Demo](https://student-performance-analysis-prediction-g5trstnyy.vercel.app/)** · 💻 **[GitHub Repository](https://github.com/yashchaudhari372-lab/Student_Performance_Analysis_Prediction)**

---

## 📌 Project Overview

**Student Performance Analysis and Prediction** is a machine learning web application designed to predict student outcomes based on academic performance, study habits, and other student-related attributes.

The application uses Python and Flask to process user inputs and generate predictions through a saved machine learning model (`model.pkl`). It provides an interactive interface where users can enter student information and explore factors associated with academic performance.

The project demonstrates the practical application of machine learning, data processing, predictive analytics, and web development by integrating a trained model into a web-based prediction system.

The application is suitable for educational demonstrations, machine learning experimentation, and data science portfolio projects.

> **Note:** Model predictions are estimates based on the model and supplied inputs. They should not be considered official academic results or used as the sole basis for educational decisions.

## ✨ Key Features

- **Student Performance Prediction:** Generates predicted student outcomes from submitted academic and student-related information.
- **Machine Learning Integration:** Uses a serialized machine learning model (`model.pkl`) to generate predictions when the model loads successfully.
- **Multiple Input Features:** Processes student attributes covering demographics, study habits, academic history, and access to resources.
- **Interactive Dashboard:** Provides a web interface for entering information and viewing prediction results.
- **Academic Performance Analysis:** Helps users explore relationships between selected student attributes and predicted outcomes.
- **Interactive Visualization:** Displays selected input features through a radar chart, making it easier to compare different student-related indicators.
- **Responsive Interface:** Designed to provide a convenient experience across different screen sizes.
- **Asynchronous Prediction Requests:** Sends prediction requests to the Flask `/predict` endpoint without requiring a complete page reload.
- **Model Status Indicator:** Displays information about whether the saved model has loaded successfully.
- **Theme Customization:** Includes selectable visual themes to personalize the dashboard.
- **Live Deployment:** Makes the application accessible online through its deployed web interface.

## 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Machine Learning | Scikit-learn |
| Numerical Processing | NumPy |
| Frontend | HTML, CSS, JavaScript |
| Data Visualization | Chart.js |
| Model Serialization | Pickle-compatible `.pkl` model |
| Application Server | Depends on the deployment configuration |
| Deployment | Vercel |
| Version Control | Git and GitHub |

## 📝 Input Features

The application processes nine student-related input features to generate a prediction.

| Feature | Description |
|---|---|
| Gender | Encoded gender selection |
| Age | Age of the student |
| Weekly Study Hours | Number of hours spent studying per week |
| Attendance Rate | Student attendance percentage |
| Parent Education Level | Education level of the student's parents |
| Internet Access | Indicates whether the student has internet access |
| Extracurricular Activities | Indicates participation in extracurricular activities |
| Previous Score | Previous academic performance score |
| Final Score (Current/Midterm) | Score entered for the current assessment |

### 🎯 Prediction Output

The application returns a predicted student status based on the submitted information and the model's output.

The result is displayed through the application's prediction interface.

**Important:** The prediction depends on the model's training process, feature encoding, and input values. The output should be interpreted as a model-generated estimate rather than a guaranteed academic outcome.

## 🔄 Prediction Workflow

The application follows an end-to-end prediction workflow:

```text
User Opens the Web Application
              ↓
Enters Student Information
              ↓
Submits the Prediction Form
              ↓
Flask Receives the Input Data
              ↓
Input Values Are Converted into Model Features
              ↓
Saved Machine Learning Model (model.pkl)
              ↓
Model Generates a Prediction
              ↓
Prediction Response Is Returned
              ↓
Dashboard Displays the Result
              ↓
Selected Features Are Visualized
```

### Workflow Explanation

1. **Data Input:** The user enters the required student-related information through the web interface.
2. **Request Processing:** The frontend submits the information to the Flask prediction endpoint.
3. **Feature Preparation:** The backend converts the submitted values into the numerical representation expected by the model.
4. **Model Inference:** The saved machine learning model processes the prepared feature vector.
5. **Prediction Generation:** The model produces the predicted result.
6. **Response Handling:** The application returns the prediction information to the frontend.
7. **Visualization:** The dashboard displays the result and visualizes selected student attributes.

The input feature order and encoding must remain consistent with those used when training the saved model.

## 📂 Repository Structure

The repository contains the following primary files:

```text
Student_Performance_Analysis_Prediction/
│
├── app.py
│   └── Flask application, user interface, and prediction endpoint
│
├── model.pkl
│   └── Serialized machine learning model
│
├── requirements.txt
│   └── Python package dependencies
│
├── vercel.json
│   └── Vercel deployment configuration
│
└── README.md
    └── Project documentation
```

## ⚙️ Installation and Local Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

Open your terminal or command prompt and execute:

```bash
git clone https://github.com/yashchaudhari372-lab/Student_Performance_Analysis_Prediction.git
```

Navigate to the project directory:

```bash
cd Student_Performance_Analysis_Prediction
```

### 2. Create a Virtual Environment

Creating a virtual environment helps isolate project dependencies.

**Windows:**

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Make sure all dependencies are installed successfully before running the application.

### 4. Run the Application

Start the Flask application:

```bash
python app.py
```

The exact startup command depends on the application's entry-point configuration.

### 5. Open the Application

If the Flask application starts using its default local development settings, open:

```text
http://127.0.0.1:5000
```

If the application specifies a different port, use the local address displayed in your terminal.

### ⚠️ Important Setup Notes

- Ensure that `model.pkl` is present in the expected location.
- Install compatible versions of Python, Flask, NumPy, and Scikit-learn.
- Keep the feature order consistent with the order used during model training.
- Load serialized pickle models only from trusted sources because loading untrusted pickle files can execute malicious code.
- The local development server should not be used as a production server.

## 🔌 Prediction API

The Flask application provides a prediction endpoint for processing student information.

| Property | Details |
|---|---|
| Endpoint | `/predict` |
| HTTP Method | `POST` |
| Framework | Flask |
| Input Format | Form-encoded data or multipart form data |
| Purpose | Generate a student outcome prediction |

### Example Request

The following example illustrates the type of request used by the prediction endpoint:

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

**Note:** This example uses illustrative input values. Verify the field names and accepted values against the current implementation in `app.py` before using the request.

### Expected Processing

The prediction endpoint processes the submitted form data and returns a response containing prediction information.

The exact response fields depend on the implementation of the Flask endpoint and the model's output.

For successful predictions, the frontend uses the returned result to update the prediction interface and relevant visualizations.

## 📊 Model Evaluation

The application integrates a saved machine learning model to generate student outcome predictions.

However, the repository's available documentation does not establish a reproducible held-out test-set evaluation with verified performance metrics.

For that reason, model accuracy, precision, recall, F1-score, and other evaluation values should not be presented as verified results without supporting experimental evidence.

### Recommended Evaluation Metrics

| Metric | Purpose |
|---|---|
| Accuracy | Measures the proportion of correct predictions for a classification model |
| Precision | Measures how many positive predictions are correct |
| Recall | Measures how many actual positive cases are identified |
| F1-Score | Combines precision and recall into a single metric |
| Confusion Matrix | Shows correct and incorrect predictions for each class |

**Important:** These metrics apply to classification tasks. If the model predicts a continuous academic score instead, regression metrics such as MAE, MSE, RMSE, and R² are more appropriate.

To evaluate the model reliably:

1. Prepare a representative dataset with known outcomes.
2. Apply the same preprocessing and feature encoding used during training.
3. Evaluate the model on data that was not used for training.
4. Calculate the metrics appropriate to the prediction task.
5. Document the evaluation dataset, methodology, and measured results.

## 🎯 Applications

The project can be used for:

- **Educational Data Analytics:** Exploring student-related attributes and academic outcomes.
- **Academic Performance Prediction:** Demonstrating how machine learning can generate predictions from student information.
- **Student Performance Exploration:** Examining academic history, study habits, and attendance as potential performance indicators.
- **Machine Learning Education:** Understanding how a trained model can be integrated into a web application.
- **Data Science Portfolio Development:** Demonstrating practical skills in Python, machine learning, and web application development.
- **Interactive Analytics:** Presenting selected student features through visualizations.

The application is intended for educational and demonstration purposes and is not a substitute for professional academic assessment.

## 🚀 Future Improvements

The project can be enhanced through the following improvements:

- **Model Evaluation:** Publish verified performance metrics and a reproducible evaluation report.
- **Input Validation:** Add robust validation for missing values, invalid inputs, and out-of-range values.
- **Model Explainability:** Introduce appropriate feature-importance or explainability methods to help users understand model behavior.
- **Prediction Insights:** Provide clear explanations of the prediction output and its limitations.
- **Enhanced Visualizations:** Add more charts for comparing academic history, attendance, and study habits.
- **Improved Error Handling:** Provide meaningful error messages when model loading or prediction fails.
- **Model Versioning:** Document the model training process, dataset source, preprocessing steps, and compatible library versions.
- **Testing:** Add unit tests for input validation, model loading, and prediction functionality.
- **Security:** Strengthen request validation and production configuration.
- **Accessibility:** Improve keyboard navigation, form labels, and compatibility with assistive technologies.
- **Fairness and Privacy:** Assess potential bias and protect student information before considering real-world educational use.

## 🛠️ Skills Demonstrated

This project demonstrates practical experience with:

- Python Programming
- Machine Learning Model Integration
- Scikit-learn
- Flask Web Application Development
- Numerical Data Processing
- Input Feature Preparation
- Prediction API Development
- HTML, CSS, and JavaScript
- Interactive Data Visualization
- Model Serialization and Loading
- Git and GitHub
- Web Application Deployment
- Technical Documentation

## 🌐 Live Demo

Try the deployed application:

### 🚀 [Student Performance Analysis and Prediction — Live Application](https://student-performance-analysis-prediction-g5trstnyy.vercel.app/)

Explore the application by entering student-related information and examining the prediction generated by the model.

**Live Application:** [Open Project](https://student-performance-analysis-prediction-g5trstnyy.vercel.app/)

**Source Code:** [View GitHub Repository](https://github.com/yashchaudhari372-lab/Student_Performance_Analysis_Prediction)

## 👨‍💻 Author

**Siddhesh**

Aspiring Data Scientist | Data Analyst | Machine Learning Enthusiast

Interested in data analysis, machine learning, predictive modeling, and building interactive data-driven applications.

- 💻 **GitHub:** [Siddhesh030](https://github.com/Siddhesh030)
- 🚀 **Live Project:** [Student Performance Analysis and Prediction](https://student-performance-analysis-prediction-g5trstnyy.vercel.app/)

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Implement and test your improvements.
4. Commit your changes with a descriptive message.
5. Push your branch to GitHub.
6. Open a pull request describing your contribution.

## 📄 License

No specific license has been verified for this repository. Before reusing, modifying, or redistributing the project, check the repository's license information and ensure that your intended use is permitted.

---

⭐ **If you find this project useful, consider starring the [GitHub repository](https://github.com/yashchaudhari372-lab/Student_Performance_Analysis_Prediction)!**
