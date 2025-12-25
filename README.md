# ⚡ Engineering-Grade Smart Home VUI & Energy Monitor

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/VUI-SpeechRecognition-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Engineering-3--Phase_Logic-red?style=for-the-badge" />
</p>

## 🌟 Project Overview
This is a sophisticated **Home Energy Management System (HEMS)** simulation. Unlike basic smart home apps, this project implements industrial electrical standards including 3-phase load balancing, MCB/RCCB safety protocols, and a tiered billing engine.

---

## 🛠️ Key Engineering Features

* **🎙️ Voice User Interface (VUI)**: Context-aware command parsing (e.g., "Turn on Study Room AC").
* **🔌 3-Phase Distribution**: Rooms are divided across **Red, Yellow, and Blue** phases to simulate real-world load balancing.
* **🛡️ Safety Simulation**: Includes a functional **Main Breaker (MCB)**. Power will not flow to devices if the breaker is tripped.
* **💰 Dynamic Billing Engine**: 
    * 0-100 Units: ₹2.00/kWh
    * 100+ Units: ₹5.00/kWh
* **📊 Live Telemetry**: Real-time calculation of Load (Watts), Consumption (kWh), and Cost (INR).

---

## 🏗️ Electrical Layout
| Phase | Rooms Assigned | Color Code |
| :--- | :--- | :--- |
| **R-Phase** | Hall, Study Room | 🔴 Red |
| **Y-Phase** | Bedroom 1, Kitchen | 🟡 Yellow |
| **B-Phase** | Bedroom 2, Bathroom | 🔵 Blue |

---

## 🚀 Installation & Usage

1. **Clone the Repo**:
   `git clone https://github.com/SIDDUSPACE/Voice-Control-Home.git`

2. **Install Dependencies**:
   `pip install SpeechRecognition pyttsx3 pyaudio`

3. **Run the Monitor**:
   `python virtual_home_pro.py`

---
<p align="right">Developed by <b>Siddarth S</b> (SIDDUSPACE)</p>