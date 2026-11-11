Industrial Predictive Maintenance Using Machine Learning



1\. Project Overview



An end-to-end Industrial Predictive Maintenance application that uses machine sensor data to predict potential machine failures.



The project demonstrates how Machine Learning can support industrial asset monitoring, condition-based maintenance and proactive maintenance planning.



The solution uses the AI4I 2020 Predictive Maintenance Dataset and provides an interactive Streamlit application for individual and batch machine predictions.



2\. Business Problem



Unexpected machine failures can cause production downtime, maintenance costs and operational disruption.



Traditional preventive maintenance often relies on fixed maintenance schedules rather than actual machine operating conditions.



This project explores a data-driven approach that analyses industrial sensor measurements to identify potential machine failures.



3\. Dataset



Dataset: AI4I 2020 Predictive Maintenance Dataset



Target variable: "Machine failure"



Input features:



\- Type

\- Air temperature \[K]

\- Process temperature \[K]

\- Rotational speed \[rpm]

\- Torque \[Nm]

\- Tool wear \[min]



Failure-mode indicators and identifier columns are excluded from the model inputs to avoid target leakage and inappropriate identifier-based learning.



4\. Project Workflow



1\. Dataset understanding and exploratory data analysis.

2\. Data quality checks and preprocessing.

3\. Feature selection and train-test splitting.

4\. Model development and comparison.

5\. Stratified cross-validation.

6\. Model selection and decision-threshold optimisation.

7\. Final model evaluation.

8\. Model interpretation using permutation importance.

9\. Model serialization using Joblib.

10\. Reusable prediction module with input validation.

11\. Automated unit testing.

12\. Streamlit application development.



5\. Machine Learning Models



The project evaluates:



\- Logistic Regression

\- Decision Tree

\- Random Forest



The final model is selected using cross-validation results and validation-based threshold optimisation.



6\. Evaluation



The project evaluates classification performance using:



\- Accuracy

\- Precision

\- Recall

\- F1-score

\- ROC-AUC

\- Average Precision



Confusion matrices are used to analyse false positives and false negatives.



The decision threshold is selected using validation data rather than automatically assuming 0.5.



7\. Application Features



Dashboard



Industrial predictive maintenance application overview.



Single Machine Prediction



Enter machine sensor readings and obtain:



\- Failure probability

\- Predicted failure status

\- Machine status alert



Batch Machine Prediction



Upload a CSV containing multiple machine records, generate predictions and download the results.



8\. Technology Stack



\- Python

\- Pandas and NumPy

\- Scikit-learn

\- Matplotlib and Seaborn

\- Joblib

\- Streamlit

\- Jupyter Notebook

\- PyCharm



9\. Project Structure



industrial-predictive-maintenance/

├── app/

├── data/

├── images/

├── models/

├── notebooks/

├── reports/

├── src/

├── tests/

├── requirements.txt

└── README.md



10\. Installation and Execution



Clone the repository:



git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd industrial-predictive-maintenance



Create a virtual environment:



python -m venv .venv



Activate it on Windows:



.venv\\Scripts\\activate



Install dependencies:



pip install -r requirements.txt



Run the application:



python -m streamlit run app/streamlit\_app.py



Run automated tests:



python -m unittest discover -s tests -v



11\. Industrial Applications



Potential applications include:



\- Machine health monitoring

\- Predictive maintenance

\- Industrial asset management

\- Sensor-based failure detection

\- Maintenance alert generation

\- IIoT analytics platforms



12\. Future Enhancements



\- Real-time industrial sensor integration using OPC UA or Modbus.

\- Integration with IIoT platforms such as PTC ThingWorx.

\- Historical sensor trend analysis.

\- Machine-wise health monitoring.

\- Cloud-based model deployment.

\- Model drift monitoring and retraining workflows.



13\. Dataset Reference

AI4I 2020 Predictive Maintenance Dataset, UCI Machine Learning Repository:

https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset

14\. Disclaimer

This is a machine-learning portfolio project developed using a public dataset. Predictions are model estimates and should not be treated as guaranteed failure forecasts or used as the sole basis for safety-critical maintenance decisions.

