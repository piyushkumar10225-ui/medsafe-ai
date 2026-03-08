# MedSafe AI

## Description
MedSafe AI is an intelligent medicine safety and prescription analysis platform built with Streamlit. It assists users in understanding medicines, prescriptions, symptoms, side effects, and potential emergency risks through AI-powered explanations and rule-based safety logic.

**Disclaimer**: MedSafe AI provides educational health information and does not replace professional medical advice.

## Features
- **Medicine Interaction Checker:** Detect known drug interactions using fuzzy matching.
- **Prescription OCR Analyzer:** Extract text from uploaded prescription images using Tesseract OCR.
- **Symptom & Doubt Solver:** Analyze symptoms with rule-based systems to provide advice and emergency warnings.
- **Side Effect Monitor:** Compare experienced symptoms with known side effects of medicines.
- **Emergency Risk Predictor:** Calculate health risk scores based on user inputs.

## Prerequisites
- Python 3.10+
- [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.
- [Ollama](https://ollama.com/) running locally with the `llama3` model pulled (`ollama run llama3`).

## Installation
1. Clone this repository or download the source code.
2. Navigate to the project directory:
   ```bash
   cd MedSafeAI
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit application:
```bash
streamlit run app.py
```
