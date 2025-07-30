import pandas as pd
import os
from datetime import datetime

DATA_PATH = "users.csv"

# --- File Setup ---
def ensure_user_file():
    if not os.path.exists(DATA_PATH) or os.stat(DATA_PATH).st_size == 0:
        df = pd.DataFrame(columns=["username", "password", "email", "role", "created_at"])
        df.to_csv(DATA_PATH, index=False)

# --- Load Users ---
def load_users():
    ensure_user_file()
    return pd.read_csv(DATA_PATH)

# --- Login Logic ---
def login(username, password):
    df = load_users()
    user = df[(df["username"] == username) & (df["password"] == password)]
    if not user.empty:
        return True, "Login successful!"
    else:
        return False, "Invalid username or password"

# --- Signup Logic ---
def signup(username, password, email="", role="user"):
    df = load_users()
    if username in df["username"].values:
        return False, "Username already exists"
    
    new_user = pd.DataFrame([{
        "username": username,
        "password": password,
        "email": email,
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return True, "Signup successful!"

# --- Optional: Get user info ---
def get_user_info(username):
    df = load_users()
    user = df[df["username"] == username]
    return user.to_dict(orient="records")[0] if not user.empty else None
