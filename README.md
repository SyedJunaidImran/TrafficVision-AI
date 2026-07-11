# 🚦 TrafficVision AI

> **AI-Based Intelligent Traffic Monitoring & Analytics System**

TrafficVision AI is an AI-powered traffic analysis application that detects, tracks, and counts vehicles from traffic images and videos. It provides real-time traffic analytics, congestion analysis, interactive dashboards, and downloadable PDF/CSV reports using modern computer vision techniques.

---

## 📌 Features

- 🚗 Vehicle Detection using **YOLOv8**
- 🎯 Multi-Object Tracking
- 📊 Automatic Vehicle Counting
- 🚦 Traffic Density Analysis
- 📈 Interactive Dashboard with Plotly
- 🖼️ Image Analysis
- 🎥 Video Analysis
- 📄 PDF Report Generation
- 📥 CSV Report Download
- 🔄 Reset & Re-analyze Files
- 🌙 Modern Streamlit UI

---

## 🖥️ Dashboard Preview

The application provides:

- Live traffic analysis
- Vehicle count statistics
- Traffic density gauge
- Vehicle distribution chart
- Traffic trend graph
- PDF & CSV reports

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| YOLOv8 | Vehicle Detection |
| OpenCV | Image & Video Processing |
| Streamlit | Web Application |
| Plotly | Interactive Charts |
| Pandas | Data Analysis |
| ReportLab | PDF Generation |

---

## 📂 Project Structure

```
TrafficVision-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── css/
│   └── style.css
│
├── models/
│   └── yolov8n.pt
│
├── src/
│   ├── detector.py
│   ├── tracker.py
│   ├── counter.py
│   ├── density.py
│   ├── dashboard.py
│   ├── report_generator.py
│   └── video_processor.py
│
├── data/
│   ├── inputs/
│   ├── outputs/
│   └── reports/
│
└── test_tracker.py
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/SyedJunaidImran/TrafficVision-AI.git
```

```bash
cd TrafficVision-AI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## 📊 Output

The application generates:

- Vehicle Counts
- Traffic Density
- Congestion Level
- Interactive Charts
- PDF Reports
- CSV Reports

---

## 🎯 Applications

TrafficVision AI can be used for:

- Smart Traffic Monitoring
- Traffic Analytics
- Urban Traffic Planning
- CCTV Traffic Analysis
- Congestion Monitoring
- Highway Monitoring
- Smart City Projects
- Event Traffic Management
- Transportation Research

---

## 🔮 Future Enhancements

- 🚑 Emergency Vehicle Detection
- 🚦 Automatic Traffic Signal Control
- 🚗 Speed Estimation
- 🔢 Number Plate Recognition (ANPR)
- 🚨 Accident Detection
- 📡 Live CCTV Integration
- ☁️ Cloud Deployment
- 📱 Mobile Application

---

## 👨‍💻 Author

**Syed Junaid**

B.Tech Computer Science & Engineering

Presidency University, Bengaluru

GitHub: https://github.com/SyedJunaidImran

---

## 📄 License

This project is developed for educational and academic purposes.

---

## ⭐ If you found this project useful, consider giving it a Star!
