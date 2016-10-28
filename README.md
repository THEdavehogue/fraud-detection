Galvanize Data Science Immersive: Fraud Detection Case Study

This repository contains files for a Fraud Detection Case Study completed by students in Galvanize's Data Science Immersive program.

In this case study, a team of four students worked with a real dataset from a mainstream online event platform to predict cases of fraud. In this context, fraud occurs any time an event organizer creates an event with the intention of selling tickets without actually hosting the event.

After analyzing more than 10,000 events, the team has created a machine-learning algorithm that can detect fraud with nearly 99% accuracy. Additionally, the model takes the expected cost/benefit of investigating fraud into account and classifies events based on the maximum benefit likely to be conferred. Given the high cost associated with reimbursing victims of fraud, our model has the potential to save hundreds of thousands of dollars for the company.

This repository contains the following files:

- Fraud_Detection_Case_Study.pdf: Slideshow with summary of methodology and findings
- model.py: Python script that imports event data, builds the model for fraud detection, and stores model for later use
- predict.py: Python script that reads in a single event and uses the pre-stored model to predict probability that the event is fraud
- scrub_data.py: Python script called by both model.py and predict.py to clean input data and engineer features to before passing data to the model builder (model.py) or predictor (predict.py)
- app.py: Overarching Python script that coordinates tasks and posted results to an online dashboard.

Notes:

- Due to the sensitive nature of this topic, this repository does not contain any raw data.
- The web app is designed to be used with data streaming from a local server and cannot be accessed outside of Galvanize.
