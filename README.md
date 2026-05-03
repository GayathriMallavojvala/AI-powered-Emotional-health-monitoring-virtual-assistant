# AI-Powered Emotional Health Monitoring Assistant

## Overview
This project is a web-based AI system designed to monitor emotional health through user interactions. It leverages Natural Language Processing (NLP) and a deep learning model (LSTM) to analyze user input, detect sentiment, and identify potential psychological risks.

The system provides an accessible and non-judgmental interface for users to express their emotions while enabling early detection of mental health concerns.
## Features
* Chatbot-based interaction for emotional support
* Sentiment and intent classification using NLP
* Detection of potential psychological risk patterns
* User authentication (login and registration)
* Web interface built using Django


## Machine Learning Approach
* Text preprocessing: cleaning, tokenization, sequence padding
* Label encoding for intent classification
* LSTM-based neural network for sequence modeling
* Softmax layer for multi-class prediction

## Tech Stack
* Backend: Django (Python)
* Machine Learning: TensorFlow / Keras (LSTM)
* NLP: Tokenization and sequence modeling
* Frontend: HTML, CSS
* Database: SQLite

## Project Structure
├── application/                # Django app (views, models, logic)
├── Mental_Health_Support/     # Project configuration
├── templates/                 # HTML templates
├── static/                    # Static assets (images, files)
├── manage.py
├── requirements.txt

## Setup Instructions
1. Clone the repository:
git clone https://github.com/GayathriMallavojvala/emotional-health-ai-assistant.git
2. Navigate to the project directory:
cd emotional-health-ai-assistant
3. Install dependencies:`
pip install -r requirements.txt
4. Run the development server:
python manage.py runserver
5. Open in browser:
http://127.0.0.1:8000/

## Notes
* Model files (.h5) are not included in this repository.
* The chatbot uses an intent-based dataset (`intents.json`) for training and response generation.

## Future Improvements
* Real-time emotion detection
* Voice-based interaction
* Integration with mental health professionals
* Deployment on cloud platforms


## Author

Gayathri Mallavojvala
