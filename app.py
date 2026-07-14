import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
import google.generativeai as genai
import shap
import matplotlib.pyplot as plt


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CreditLens AI",
    page_icon="💳",
    layout="wide"
)

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0B1020, #111827);
    color: white;
}

/* Titles */
h1 {
    color: white !important;
    text-align: center;
}

/* Input Labels */
label {
    color: white !important;
    font-weight: 600;
}

/* Text Inputs */
.stTextInput input,
.stNumberInput input {
    background-color: #1E293B !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

/* Selectboxes */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1E293B !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg,#2563EB,#7C3AED);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-weight: bold;
    font-size: 16px;
}

.stButton > button:hover {
    transform: scale(1.02);
}

/* Metrics */
div[data-testid="metric-container"] {
    background: #1E293B;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)


import google.generativeai as genai

# -----------------------------------------
# GEMINI CONFIG
# -----------------------------------------

gemini_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=gemini_key)

gemini = genai.GenerativeModel("gemini-2.5-flash")




# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    model = joblib.load("credit_model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")
    return model, preprocessor

model, preprocessor = load_model()





# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

if not st.session_state.logged_in:

    st.markdown("""
       <h1 style='text-align:center;'>
        🔐   CreditLens AI Login
        </h1>
        """, unsafe_allow_html=True)

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid Credentials")

    st.stop()




# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💳 CreditLens AI")
st.markdown(
    "Predict whether a customer is creditworthy based on financial history."
)

# --------------------------------------------------
# INPUTS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    person_age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    person_income = st.number_input(
        "Annual Income",
        min_value=1000,
        value=50000
    )

    person_emp_length = st.number_input(
        "Employment Length (Years)",
        min_value=0.0,
        value=5.0
    )

    loan_amnt = st.number_input(
        "Loan Amount",
        min_value=100,
        value=10000
    )

with col2:

    loan_int_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        value=10.5
    )

    loan_percent_income = st.number_input(
        "Loan Percent Income",
        min_value=0.0,
        value=0.20
    )

    cb_person_cred_hist_length = st.number_input(
        "Credit History Length",
        min_value=1,
        value=5
    )

# --------------------------------------------------
# CATEGORICAL INPUTS
# --------------------------------------------------

person_home_ownership = st.selectbox(
    "Home Ownership",
    ["RENT", "OWN", "MORTGAGE", "OTHER"]
)

loan_intent = st.selectbox(
    "Loan Purpose",
    [
        "EDUCATION",
        "MEDICAL",
        "VENTURE",
        "PERSONAL",
        "DEBTCONSOLIDATION",
        "HOMEIMPROVEMENT"
    ]
)

loan_grade = st.selectbox(
    "Loan Grade",
    ["A", "B", "C", "D", "E", "F", "G"]
)

cb_person_default_on_file = st.selectbox(
    "Previous Default",
    ["Y", "N"]
)

# --------------------------------------------------
# PDF FUNCTION
# --------------------------------------------------

def generate_pdf(score, probability, prediction):

    pdf_file = "credit_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Credit Assessment Report")

    c.setFont("Helvetica", 12)

    c.drawString(
        100,
        760,
        f"Prediction: {'Creditworthy' if prediction == 0 else 'High Risk'}"
    )

    c.drawString(
        100,
        730,
        f"Credit Score: {score}"
    )

    c.drawString(
        100,
        700,
        f"Default Probability: {probability:.2%}"
    )

    c.save()

    return pdf_file

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if st.button("Predict Credit Worthiness"):

    data = pd.DataFrame({
        "person_age": [person_age],
        "person_income": [person_income],
        "person_emp_length": [person_emp_length],
        "loan_amnt": [loan_amnt],
        "loan_int_rate": [loan_int_rate],
        "loan_percent_income": [loan_percent_income],
        "cb_person_cred_hist_length": [cb_person_cred_hist_length],
        "person_home_ownership": [person_home_ownership],
        "loan_intent": [loan_intent],
        "loan_grade": [loan_grade],
        "cb_person_default_on_file": [cb_person_default_on_file]
    })

    processed = preprocessor.transform(data)

    prediction = model.predict(processed)[0]

    probability = model.predict_proba(processed)[0][1]

    credit_score = max(
        300,
        min(
            850,
            int(850 - (probability * 550))
        )
    )

    st.subheader("Prediction Result")

    if prediction == 0:
        st.success("✅ Creditworthy Customer")
    else:
        st.error("❌ High Risk Customer")

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            "Default Probability",
            f"{probability * 100:.2f}%"
        )

    with metric_col2:
        st.metric(
            "Credit Score",
            credit_score
        )

    # -----------------------------------------
    # GAUGE CHART (COLORED)
    # -----------------------------------------

    gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=credit_score,
    title={"text": "Credit Score"},
    gauge={
         "axis": {"range": [300, 850]},
         "bar": {"color": "darkblue"},
         "steps": [
            {"range": [300, 580], "color": "red"},
            {"range": [580, 670], "color": "orange"},
            {"range": [670, 740], "color": "yellow"},
            {"range": [740, 850], "color": "green"}
           ]
          }
        ))

    st.plotly_chart(gauge, use_container_width=True)

    

    # -----------------------------------------
    # HISTORY
    # -----------------------------------------

    st.session_state.history.append({
        "Credit Score": credit_score,
        "Probability": round(probability * 100, 2),
        "Prediction": (
            "Creditworthy"
            if prediction == 0
            else "High Risk"
        )
    })

    # -----------------------------------------
    # PDF DOWNLOAD
    # -----------------------------------------

    pdf_path = generate_pdf(
        credit_score,
        probability,
        prediction
    )

    with open(pdf_path, "rb") as file:

        st.download_button(
            label="📄 Download Credit Report",
            data=file,
            file_name="credit_report.pdf",
            mime="application/pdf"
        )


    # -----------------------------------------
    # SHAP EXPLANATION
    # -----------------------------------------

    st.subheader("🔍 Why this prediction was made")

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(processed)

    fig, ax = plt.subplots(figsize=(8, 4))

    shap.summary_plot(
        shap_values,
        processed,
        show=False
    )

    st.pyplot(fig)   
    

# -----------------------------------------
# AI FINANCIAL ADVISOR
# -----------------------------------------

    prompt = f"""
    Credit Score: {credit_score}

    Default Probability: {probability:.2%}

    Prediction:
    {"Creditworthy" if prediction == 0 else "High Risk"}

    Explain:
    1. Why customer received this score
    2. Main risk factors
    3. How to improve credit profile
     """

    st.write("Gemini initialized")
    

    try:
       response = gemini.generate_content(prompt)

       st.subheader("🤖 AI Financial Advisor")
       st.write(response.text)

    except Exception as e:
        st.error(f"Gemini Error: {e}")     

# --------------------------------------------------
# HISTORY TABLE
# --------------------------------------------------

if len(st.session_state.history) > 0:

    st.subheader("Prediction History")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )