import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.predict import predict_machine_failure

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Industrial Predictive Maintenance",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background-color: #F3F6FA;
    color: #1E293B;
}

/* Main content */
.block-container {
    padding-top: 2rem;
}

/* Main title */
.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #12304A;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    color: #526579;
    font-size: 16px;
}

/* Section headings */
.section-title {
    color: #087F8C;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE5ED;
    box-shadow: 0 2px 6px rgba(20, 50, 70, 0.08);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #526579 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #12304A !important;
    font-weight: 700;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #12304A;
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

/* General text */
.stMarkdown p {
    color: #334155;
}

/* Divider */
hr {
    border-color: #DCE5ED;
}

/* Metric value formatting */
[data-testid="stMetricValue"] {
    color: #12304A !important;
    font-weight: 700;
    font-size: 20px !important;
    white-space: normal !important;
    overflow-wrap: anywhere;
    line-height: 1.3;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🏭 Industrial AI")
st.sidebar.caption("Predictive Maintenance Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Single Machine Prediction",
        "Batch Prediction"
    ]
)

st.sidebar.markdown(
    """
    <div style="
        color: #AFC4D8;
        font-size: 13px;
        line-height: 1.6;
    ">
        AI-powered machine failure prediction
        using industrial sensor data.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":
    st.markdown(
        '<div class="main-title">'
        'Industrial Predictive Maintenance'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Machine Health Monitoring and Failure Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="section-title">Platform Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ML Model", "Loaded")

    with col2:
        st.metric("Prediction Type", "Binary Classification")

    with col3:
        st.metric("Input Features", "6")

    st.divider()

    st.subheader("About This Application")

    st.write("""
    This application uses a trained Machine Learning model
    to predict potential machine failures from industrial
    sensor measurements.

    **Input parameters:**
    - Machine Type
    - Air Temperature
    - Process Temperature
    - Rotational Speed
    - Torque
    - Tool Wear

    **Application capabilities:**
    - Individual machine failure prediction
    - Batch machine prediction
    - Failure probability estimation
    - Machine health alerts
    """)

    st.caption(
        "Model: AI4I 2020 Predictive Maintenance Dataset"
    )


# --------------------------------------------------
# SINGLE MACHINE PREDICTION PAGE
# --------------------------------------------------

elif page == "Single Machine Prediction":

    st.title("🔍 Single Machine Prediction")

    st.write(
        "Enter the sensor readings of an individual machine "
        "to predict its failure risk."
    )

    st.divider()

    with st.form("single_machine_form"):

        st.subheader("Machine Information")

        machine_type = st.selectbox(
            "Machine Type",
            ["L", "M", "H"],
            help="L = Low, M = Medium, H = High product quality variant"
        )

        st.subheader("Industrial Sensor Readings")

        col1, col2 = st.columns(2)

        with col1:
            air_temp = st.number_input(
                "Air Temperature [K]",
                min_value=0.0,
                value=300.0,
                step=0.1
            )

            rotational_speed = st.number_input(
                "Rotational Speed [rpm]",
                min_value=0.0,
                value=1500.0,
                step=1.0
            )

            tool_wear = st.number_input(
                "Tool Wear [min]",
                min_value=0.0,
                value=120.0,
                step=1.0
            )

        with col2:
            process_temp = st.number_input(
                "Process Temperature [K]",
                min_value=0.0,
                value=310.0,
                step=0.1
            )

            torque = st.number_input(
                "Torque [Nm]",
                min_value=0.0,
                value=40.0,
                step=0.1
            )

        predict_button = st.form_submit_button(
            "Predict Machine Failure",
            type="primary",
            use_container_width=True
        )

    if predict_button:

        machine_data = pd.DataFrame([{
            "Type": machine_type,
            "Air temperature [K]": air_temp,
            "Process temperature [K]": process_temp,
            "Rotational speed [rpm]": rotational_speed,
            "Torque [Nm]": torque,
            "Tool wear [min]": tool_wear
        }])

        try:
            prediction_result = predict_machine_failure(machine_data)

            probability = float(
                prediction_result["Failure Probability"].iloc[0]
            )

            predicted_failure = int(
                prediction_result["Predicted Failure"].iloc[0]
            )

            machine_status = str(
                prediction_result["Machine Status"].iloc[0]
            )

            st.divider()
            st.subheader("Machine Prediction Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Failure Probability",
                    f"{probability:.2%}"
                )

            with col2:
                st.metric(
                    "Predicted Failure",
                    "Yes" if predicted_failure == 1 else "No"
                )

            with col3:
                st.metric(
                    "Machine Status",
                    machine_status
                )

            if predicted_failure == 1:
                st.error(
                    "⚠️ Potential machine failure detected. "
                    "Inspect the machine and review its operating condition."
                )
            else:
                st.success(
                    "No failure predicted at the configured "
                    "decision threshold."
                )

            st.caption(
                "This is a model prediction, not a guarantee "
                "of actual machine condition."
            )

        except Exception as error:
            st.error(f"Prediction failed: {error}")



# --------------------------------------------------
# BATCH MACHINE PREDICTION PAGE
# --------------------------------------------------

elif page == "Batch Prediction":

    st.title("📊 Batch Machine Prediction")

    st.write(
        "Upload a CSV file containing sensor readings "
        "for multiple machines."
    )

    st.divider()

    st.subheader("Upload Machine Sensor Data")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            batch_data = pd.read_csv(uploaded_file)

            st.subheader("Uploaded Dataset")

            st.write(
                f"Total machine records: {len(batch_data)}"
            )

            st.dataframe(
                batch_data.head(10),
                use_container_width=True
            )

            predict_batch_button = st.button(
                "Predict All Machines",
                type="primary",
                use_container_width=True
            )

            if predict_batch_button:
                with st.spinner("Generating machine predictions..."):
                    prediction_results = predict_machine_failure(
                        batch_data
                    )

                    final_results = pd.concat(
                        [
                            batch_data.reset_index(drop=True),
                            prediction_results.reset_index(drop=True)
                        ],
                        axis=1
                    )

                st.success(
                    "Batch predictions generated successfully!"
                )

                st.subheader("Prediction Summary")

                total_machines = len(final_results)

                failure_count = int(
                    (final_results["Predicted Failure"] == 1).sum()
                )

                normal_count = total_machines - failure_count

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Total Machines",
                        total_machines
                    )

                with col2:
                    st.metric(
                        "Potential Failures",
                        failure_count
                    )

                with col3:
                    st.metric(
                        "No Failure Predicted",
                        normal_count
                    )

                st.subheader("Machine Prediction Results")

                st.dataframe(
                    final_results,
                    use_container_width=True
                )

                csv_output = final_results.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="Download Prediction Results",
                    data=csv_output,
                    file_name="machine_prediction_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        except Exception as error:
            st.error(f"Batch prediction failed: {error}")

    else:
        st.info(
            "Upload a CSV file to begin batch machine prediction."
        )

        st.markdown("""
        **Required CSV columns:**

        - `Type`
        - `Air temperature [K]`
        - `Process temperature [K]`
        - `Rotational speed [rpm]`
        - `Torque [Nm]`
        - `Tool wear [min]`
        """)

        st.caption(
            "Each row represents one machine. "
            "Do not include the target column Machine failure."
        )
