import pandas as pd
from sklearn.preprocessing import LabelEncoder
import sqlite3

def load_and_clean_data(csv_path=r"C:\Users\MaKsys\Desktop\purna_shah\purna\ML\mini_project\AQI_2020_to_2025_October.csv"):

    df = pd.read_csv(
        csv_path,
        sep=",",
        encoding="utf-8",
        on_bad_lines="skip",
        low_memory=False
    )

    df.ffill(inplace=True)

    # Date handling
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        df["Day"] = df["Date"].dt.day
        df.drop("Date", axis=1, inplace=True)

    # 🔥 FIX: Encode only important categorical columns
    categorical_cols = ["City", "Air Quality", "Prominent Pollutant"]

    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

    df.fillna(0, inplace=True)

    return df


# ==========================================
# FLASK APP
# ==========================================
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'aqi_analytics_secret_key_2024'

# Hardcoded fallback users (used if DB is missing or no match found)
users = {
    "admin": "1234",
    "purna": "0000"
}


def validate_user_from_db(username, password):
    """
    Check username/password in SQLite users table.
    Expected table: users(username TEXT, password TEXT)
    """
    try:
        conn = sqlite3.connect("aqi_app.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return False

        db_username, db_password = row
        return db_username == username and db_password == password
    except sqlite3.Error as e:
        print(f"[LOGIN DEBUG] SQLite error: {e}")
        return False


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Debug prints for login flow
        print(f"[LOGIN DEBUG] Received username: '{username}'")
        print(f"[LOGIN DEBUG] Received password: '{password}'")

        if not username or not password:
            flash('Invalid credentials', 'error')
            return render_template('login.html')

        db_valid = validate_user_from_db(username, password)
        fallback_valid = users.get(username) == password
        print(f"[LOGIN DEBUG] DB valid: {db_valid}, fallback valid: {fallback_valid}")

        if db_valid or fallback_valid:
            session['user'] = username
            print(f"[LOGIN DEBUG] Login success for: {username}")
            return redirect(url_for('dashboard'))

        print(f"[LOGIN DEBUG] Login failed for: {username}")
        flash('Invalid credentials', 'error')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Static, pre-formatted output only (no ML execution)
    return render_template('result.html', user=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)