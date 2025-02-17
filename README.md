# OSTDS - COVID-19 Data Analytics

This project analyzes COVID-19 data using Django for the backend and React for the frontend. It provides dynamic visual dashboards with interactive graphs and filters to explore pandemic trends.

Features

```
✅ Time Series Analysis 📈
✅ Correlation Heatmap 🔥
✅ Pie Chart for Top 10 States 🍕
✅ Geographic Spread Visualization 🌍
✅ Bar Chart for Active Cases 📊
✅ Case Fatality Ratio (CFR) ⚰️
✅ Scatter Plot for Incident Rate vs. CFR 🎯
```

```
OSTDS/
├── assign_1_corona/
│   ├── api/
│   ├── src/
│   │   ├── backend/              # Django backend for data processing
│   │   │   ├── manage.py         # Django entry point
│   │   │   ├── api/              # API views for fetching data
│   │   │   ├── models/           # Database models
│   │   │   ├── requirements.txt  # Python dependencies
│   │   ├── frontend/             # React frontend for visualizations
│   │   │   ├── src/              # Main React source code
│   │   │   ├── public/           # Static files
│   │   ├── data/                 # CSV files and datasets
│   │   ├── README.md             # Project documentation
```

## Setup Instructions

### 1️⃣ Clone the Repository
git clone https://github.com/gyandeep83/OSTDS.git
cd OSTDS

### 2️⃣ Backend Setup (Django + Python)

### 📌 Create a Virtual Environment
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux

### 📌 Install Dependencies
pip install -r backend/requirements.txt

### 📌 Run the Server
cd backend
python manage.py runserver

## 3️⃣ Frontend Setup (React + Chart.js)
cd frontend
npm install
npm start


## Usage

1. Open the frontend in a browser at http://localhost:3000
2. The backend runs at http://localhost:8000/api/
3. Use the interactive charts to explore COVID-19 data.

## Technologies Used

1. Backend: Django, Pandas, SQLite
2. Frontend: React, Chart.js, D3.js
3. Data Source: Processed COVID-19 CSV datasets

## Contributing

If you want to improve the project, feel free to fork the repo and submit a PR! 🚀

## License

This project is open-source under the MIT License.

