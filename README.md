# 🌍 AQI Analytics Flask Project

A web-based Air Quality Index (AQI) analytics system built using **Flask + Machine Learning + SQLite**.

---

## 🚀 Features

* AQI data analysis from database
* Multiple ML models:

  * Decision Tree
  * Random Forest
  * SVM
  * Logistic Regression
* Data visualization (Heatmap + Distribution)
* Login system (basic)
* Clean UI dashboard

---

## 🗂 Project Structure

```
project/
├── app.py
├── implementation.py
├── aqi_data.db
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
```

---

## ⚙️ Setup Instructions

### 1. Clone repo

```
git clone https://github.com/PurnaShah24/aqi-flask-project.git
cd aqi-flask-project
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run app

```
python app.py
```

### 4. Open browser

```
http://127.0.0.1:5000
```

---

## 📊 Sample Output

* Classification Accuracy
* Confusion Matrix
* Regression MSE
* Clustering Results

---

## ⚠️ Notes

* Uses SQLite database instead of CSV for better performance
* Large dataset optimized (avoids memory crash)
* Uses Label Encoding instead of one-hot encoding

---

## 👨‍💻 Author

Purna Shah
