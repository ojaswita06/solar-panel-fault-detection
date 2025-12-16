# 🌞 Solar Panel Fault Detection System

## Overview
This project implements a machine learning-based system to detect faults in solar panels using sensor data such as power output, temperature, and irradiation.

## Features
- Fault detection using supervised machine learning
- Fault severity classification (LOW / HIGH)
- Data visualization of faulty vs normal panels
- Interactive Streamlit dashboard
- Model persistence for reuse

## Technologies Used
- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib
- Streamlit

## How It Works
1. Sensor data is collected
2. Fault labels are generated based on power loss
3. A Decision Tree model is trained
4. The model predicts faults on new data
5. Results are displayed via a web app

## Usage
```bash
python main.py
streamlit run app.py
