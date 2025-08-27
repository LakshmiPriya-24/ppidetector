pii_detector_and_redactor
Project Guardian 2.0: Real-time PII Defense

This repository contains the solution for the "Real-time PII Defense" challenge, a technical exercise focused on identifying and redacting Personally Identifiable Information (PII) from data streams and proposing a robust deployment strategy.

PII Detector & Redactor
The core of the solution is a Python script that processes a CSV file, detects PII based on a strict set of definitions, and generates a new CSV with the PII redacted and a new column indicating whether PII was found in each record. File:detector_Lakshmipriya.py`

This script implements the following logic:

PII Definitions: The code adheres to the challenge's definitions of Standalone PII (e.g., Aadhar, Phone Number) and Combinatorial PII (e.g., Name + Email).
Detection: It uses Python's re module with carefully crafted regular expressions to accurately identify PII patterns.
Redaction: It redacts the identified PII, replacing it with masked versions or a [REDACTED_PII] placeholder to prevent data leakage.
Output: It generates a new CSV file named redacted_output_candidate_full_name.csv with the record_id, redacted_data_json, and a boolean is_pii column.
Execution

To run the detector, use the following command: python3 detector_Lakshmipriya.py iscp_pii_dataset.csv redacted_output_Lakshmipriya.csv

Deployment Strategy
howitisusedpii_detector_and_redactor
Project Guardian 2.0: Real-time PII Defense

This repository contains the solution for the "Real-time PII Defense" challenge, a technical exercise focused on identifying and redacting Personally Identifiable Information (PII) from data streams and proposing a robust deployment strategy.

PII Detector & Redactor
The core of the solution is a Python script that processes a CSV file, detects PII based on a strict set of definitions, and generates a new CSV with the PII redacted and a new column indicating whether PII was found in each record. File:detector_Lakshmipriya.py`

This script implements the following logic:

PII Definitions: The code adheres to the challenge's definitions of Standalone PII (e.g., Aadhar, Phone Number) and Combinatorial PII (e.g., Name + Email).
Detection: It uses Python's re module with carefully crafted regular expressions to accurately identify PII patterns.
Redaction: It redacts the identified PII, replacing it with masked versions or a [REDACTED_PII] placeholder to prevent data leakage.
Output: It generates a new CSV file named redacted_output_candidate_full_name.csv with the record_id, redacted_data_json, and a boolean is_pii column.
Execution

To run the detector, use the following command: python3 detector_Lakshmipriya.py iscp_pii_dataset.csv redacted_output_Lakshmipriya.csv

Deployment Strategy
<img width="2048" height="2048" alt="howitisused" src="https://github.com/user-attachments/assets/0c447847-3115-475f-bd6f-4933af089f18" />

As depicted in the diagram, raw client data that is possibly carrying PII first reaches the API Gateway. The PII Redaction Plugin, where our Python code resides, is called at this point. It inspects the incoming payload, identifies and marks out any PII, and then passes the cleansed data to the corresponding backend microservice. This has the effect of only ever exposing backend services and their respective logs and databases to data that is PII-free.

Justification Scalability An API Gateway is designed to support heavy loads of traffic and scale horizontally. By having the PII solution integrated as a plugin, it inherits this built-in scalability and does not become a bottleneck as the traffic increases for the PII defense system.

Latency The core strength of the solution is real-time processing. Positioning it at the API Gateway reduces latency by fixing the problem at the first point of data flow. The code given, which is based on low-latency regex matching and dictionary lookups, is tuned for this low-latency environment.

Cost-Effectiveness
A centralized API Gateway plugin is a cost-effective solution. Instead of running a separate sidecar container for each service, one central instance of the PII defense logic protects the entire platform's ingress. This arrangement reduces the operational burden and lowers infrastructure costs.

Ease of Integration
Deploying the solution to the API Gateway is a non-invasive method that does not need changes to the existing application code. This advantage is significant in a large and complex microservices environment like Flixkart's, where changing each application can take a lot of time and lead to mistakes.
As depicted in the diagram, raw client data that is possibly carrying PII first reaches the API Gateway. The PII Redaction Plugin, where our Python code resides, is called at this point. It inspects the incoming payload, identifies and marks out any PII, and then passes the cleansed data to the corresponding backend microservice. This has the effect of only ever exposing backend services and their respective logs and databases to data that is PII-free.

Justification Scalability An API Gateway is designed to support heavy loads of traffic and scale horizontally. By having the PII solution integrated as a plugin, it inherits this built-in scalability and does not become a bottleneck as the traffic increases for the PII defense system.

Latency The core strength of the solution is real-time processing. Positioning it at the API Gateway reduces latency by fixing the problem at the first point of data flow. The code given, which is based on low-latency regex matching and dictionary lookups, is tuned for this low-latency environment.

Cost-Effectiveness
A centralized API Gateway plugin is a cost-effective solution. Instead of running a separate sidecar container for each service, one central instance of the PII defense logic protects the entire platform's ingress. This arrangement reduces the operational burden and lowers infrastructure costs.

Ease of Integration
Deploying the solution to the API Gateway is a non-invasive method that does not need changes to the existing application code. This advantage is significant in a large and complex microservices environment like Flixkart's, where changing each application can take a lot of time and lead to mistakes.
