# AI-Powered Cyberattack Detection in a Simulated Banking Environment

This project demonstrates how Artificial Intelligence (AI) can be applied to **real-time cyberattack detection** through a full-stack simulation, including a banking application, a monitoring API with machine learning, and a live threat dashboard.

---

## Overview

The project simulates a real-world scenario where a **bank web application** is monitored by an **AI-based detection system** capable of identifying **brute force**, **SQL injection**, **DDoS**, and other attacks in real time. The monitoring system uses machine learning/deep learning models and provides a clear **visual dashboard** for alerts and traffic analytics.

---

## Components

### 1. Bank Client App

A simple demo web application mimicking a client-facing banking portal.

- **Frontend**: HTML + TailwindCSS + JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite

**Features**:

- Fake login and dashboard pages
- Sends every request as a log to the monitoring API
- Simulates sensitive banking functionality like transfers

---

### 2. Monitoring API

A backend system that receives traffic logs and classifies them as normal or malicious using an AI model.

- **Framework**: FastAPI (Python)

**Responsibilities**:

- Log ingestion & validation
- AI-based classification
- Writing results to monitoring database
- Broadcasting alerts to the frontend

---

### 3. AI/ML Model

A pre-trained model used to classify incoming logs.

- **Frameworks**: Scikit-learn / Keras / TensorFlow
- **Types of attacks detected**:
  - Brute force (multiple failed logins)
  - SQL Injection
  - DDoS (request frequency anomalies)
- **Output**:
  - Class label
  - Confidence score

---

### 4. Monitoring Dashboard

A real-time dashboard for administrators.

- **Frontend**: React + TailwindCSS
- **Features**:
  - Live traffic logs (via WebSocket)
  - Real-time alerts for detected attacks
  - Charts (attack frequency, types, IP distribution)
  - Filtering, searching, stats

---

### 5. Monitoring Database

Stores traffic logs, detection results, and alerts.

- **Engine**: SQLite
- **Tables**:
  - `logs`: stores raw traffic
  - `detections`: AI model outputs
  - `alerts`: attack metadata for the dashboard

---

## System Architecture

```mermaid
graph TD
A[User interacts with Bank App] --> B[Flask Backend]
B --> C[Monitoring API (FastAPI)]
C --> D[AI Model Prediction]
D --> E[Monitoring Database]
E --> F[Real-Time Dashboard]
```
