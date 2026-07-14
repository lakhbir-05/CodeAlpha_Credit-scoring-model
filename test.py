# 💳 CreditLens AI

An AI-powered **Credit Risk Assessment System** . The application predicts whether a loan applicant is **Creditworthy** or **High Risk** based on their financial profile. It also provides an estimated credit score, default probability, AI-generated financial advice using **Google Gemini**, SHAP explainability, and downloadable PDF reports.

---

# 🚀 Features

- 🔐 Secure Login Authentication
- 💳 Credit Risk Prediction
- 📊 Credit Score Estimation
- 📈 Default Probability Prediction
- 📉 Interactive Credit Score Gauge
- 🔍 SHAP Explainable AI
- 🤖 AI Financial Advisor (Google Gemini)
- 📄 PDF Credit Assessment Report
- 📜 Prediction History
- 🎨 Modern Responsive Streamlit UI

---

# 🛠️ Tech Stack

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- Python

### Machine Learning
- Scikit-learn
- CatBoost
- XGBoost
- Random Forest
- Gradient Boosting
- Logistic Regression
- LightGBM
- Extra Trees
- Stacking Classifier

### Explainable AI
- SHAP

### Data Processing
- Pandas
- NumPy

### Visualization
- Plotly
- Matplotlib

### AI Integration
- Google Gemini API

### Report Generation
- ReportLab

---

# 📂 Project Structure

```
CREDIT/
│
├── app.py
├── credit_model.pkl
├── preprocessor.pkl
├── requirements.txt
├── README.md
└── .streamlit/
```

---

# 📊 Dataset

**Dataset:** Credit Risk Dataset

The dataset contains customer financial information including:

- Age
- Annual Income
- Employment Length
- Loan Amount
- Interest Rate
- Loan Purpose
- Home Ownership
- Loan Grade
- Previous Default History
- Credit History Length
- Loan Percentage of Income

Target Variable:

- **0 → Creditworthy**
- **1 → High Risk**

---

# 🤖 Machine Learning Pipeline

### Data Preprocessing

- Duplicate Removal
- Missing Value Handling (KNN Imputer)
- Standard Scaling
- One-Hot Encoding
- Column Transformer Pipeline

---

### Models Evaluated

- Logistic Regression
- Support Vector Machine (SVM)
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM
- Voting Classifier
- **Stacking Classifier (Final Model)**

---

# 📈 Model Performance

| Model | Accuracy |
|--------|----------|
| Stacking Classifier | **93.91%** |

The final deployed model is a **Stacking Classifier**, combining multiple machine learning algorithms to achieve high predictive performance.

---

# 💻 Installation

## Clone Repository

```bash
git clone <repository_url>
```

---

## Move into Project Folder

```bash
cd CREDIT
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 🔐 Login Credentials

```
Username : admin

Password : admin123
```

---

# 📋 User Inputs

The application predicts credit risk using the following customer information:

- Age
- Annual Income
- Employment Length
- Loan Amount
- Interest Rate
- Loan Percentage of Income
- Credit History Length
- Home Ownership
- Loan Purpose
- Loan Grade
- Previous Loan Default

---

# 📊 Prediction Output

The application provides:

- ✅ Creditworthy / High Risk Prediction
- 📈 Default Probability
- 💳 Estimated Credit Score
- 📊 Interactive Credit Score Gauge
- 🔍 SHAP Feature Importance
- 🤖 AI Financial Advice
- 📄 Downloadable PDF Report

---

# 🔍 Explainable AI

The system uses **SHAP (SHapley Additive Explanations)** to explain the contribution of each input feature toward the final prediction, improving transparency and interpretability.

---

# 🤖 AI Financial Advisor

The application integrates **Google Gemini AI** to generate personalized financial recommendations based on the predicted credit score and default probability.

The AI provides:

- Explanation of the prediction
- Key financial risk factors
- Suggestions to improve the customer's credit profile

---

# 📄 PDF Report

A downloadable report is generated containing:

- Prediction Result
- Credit Score
- Default Probability

---

# 📦 Required Libraries

- streamlit
- pandas
- numpy
- scikit-learn
- joblib
- shap
- matplotlib
- plotly
- reportlab
- google-generativeai
- xgboost
- catboost
- lightgbm

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 🎯 Future Enhancements

- User Registration
- Database Integration
- Loan Approval Recommendation
- Email Report Sharing
- Dashboard Analytics
- Cloud Deployment
- Real-time API Integration
- Multi-language Support

---

# 👩‍💻 Developed By

**Lakhbir Kaur**

B.Tech Computer Science & Engineering

Punjabi University, Patiala

---

# 📜 License

This project is developed for educational and academic purposes.
