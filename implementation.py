# =========================================
# 1. IMPORT LIBRARIES
# =========================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix

# Models
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans, AgglomerativeClustering

# =========================================
# 2. LOAD DATA (FIXED)
# =========================================
import sqlite3

conn = sqlite3.connect("aqi_data.db")
df = pd.read_sql_query("SELECT * FROM aqi_records", conn)
conn.close()

print("Dataset Preview:\n", df.head())
print("\nMissing Values:\n", df.isnull().sum())

# =========================================
# 3. DATA CLEANING + FEATURE ENGINEERING
# =========================================

# Step 1: Fill missing values (initial)
df.ffill(inplace=True)

# Step 2: Convert Date column safely
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Step 3: REMOVE rows where Date is invalid (VERY IMPORTANT)
df = df.dropna(subset=['Date'])

# Step 4: Extract features from Date
df['Year'] = df['Date'].dt.year
df['Month_num'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# Step 5: Drop original Date
df.drop('Date', axis=1, inplace=True)

# Step 6: Encode categorical columns
df = pd.get_dummies(df, drop_first=True)

# Step 7: FINAL NaN CLEANING (MOST IMPORTANT 🔥)
df = df.fillna(0)

# Check
print("\nRemaining NaN values:\n", df.isnull().sum())
print("\nAfter Encoding:\n", df.head())
# =========================================
# 4. VISUALIZATION
# =========================================
plt.figure(figsize=(10,8))
sns.heatmap(df.corr(), cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

sns.histplot(df['AQI Value'], kde=True)
plt.title("AQI Distribution")
plt.show()

# =========================================
# 5. FEATURE & TARGET
# =========================================
target = 'AQI Value'

# Classification labels
def categorize_aqi(aqi):
    if aqi <= 50:
        return 0
    elif aqi <= 100:
        return 1
    else:
        return 2

df['AQI_Category'] = df[target].apply(categorize_aqi)

# Features
X = df.drop([target, 'AQI_Category'], axis=1)
y_class = df['AQI_Category']
y_reg = df[target]

# =========================================
# 6. TRAIN TEST SPLIT
# =========================================
X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42)

# Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================================
# 7. CLASSIFICATION MODELS
# =========================================
models = {
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes": GaussianNB()
}

print("\n===== CLASSIFICATION RESULTS =====")
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{name} Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# Confusion Matrix (Random Forest)
best_model = RandomForestClassifier()
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# =========================================
# 8. REGRESSION
# =========================================
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X, y_reg, test_size=0.2, random_state=42)

model_reg = LinearRegression()
model_reg.fit(X_train_r, y_train_r)
y_pred_r = model_reg.predict(X_test_r)

print("\n===== REGRESSION RESULT =====")
print("MSE:", mean_squared_error(y_test_r, y_pred_r))

# =========================================
# 9. CLUSTERING
# =========================================
# Use scaled data for clustering
X_scaled = StandardScaler().fit_transform(X)

# K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
df['KMeans_Cluster'] = kmeans.fit_predict(X_scaled)

# Agglomerative
agg = AgglomerativeClustering(n_clusters=3)
df['Agg_Cluster'] = agg.fit_predict(X_scaled)

print("\nClustering Completed")

# =========================================
# 10. CLUSTER VISUALIZATION
# =========================================
plt.scatter(X_scaled[:,0], X_scaled[:,1], c=df['KMeans_Cluster'])
plt.title("K-Means Clustering")
plt.show()

plt.scatter(X_scaled[:,0], X_scaled[:,1], c=df['Agg_Cluster'])
plt.title("Agglomerative Clustering")
plt.show()

# =========================================
# DONE ✅
# =========================================
print("\n✅ ALL EXPERIMENTS COMPLETED SUCCESSFULLY")