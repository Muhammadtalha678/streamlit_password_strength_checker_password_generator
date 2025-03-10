import re
import streamlit as st
import string
import secrets
import os
import json
import requests
PASSWORD_HISTORY_FILE = "password_history.json"

# 🔹 Get user's unique identifier (IP-based method)
def get_user():
    try:
        response = requests.get("https://api64.ipify.org?format=json")  
        return response.json()["ip"]  # Use IP as user ID
    except:
        return "unknown_user"  # Default if IP fetch fails

# 🔹 Load existing password history
def load_password_history():
    if os.path.exists(PASSWORD_HISTORY_FILE):
        try:
            with open(PASSWORD_HISTORY_FILE, "r") as file:
                content = file.read().strip()  # Read and remove extra spaces/newlines
                return json.loads(content) if content else {}  # Return {} if file is empty
        except json.JSONDecodeError:
            return {}  # If JSON is corrupted, return empty dictionary
    return {}

# 🔹 Save password history
def save_password_history(history):
    with open(PASSWORD_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# 🔹 Check if password was used before
def is_reused_password(user, password):
    history = load_password_history()
    return user in history and password in history[user]

# 🔹 Add password to history (only last 10)
def update_password_history(user, password):
    history = load_password_history()
    
    if user not in history:
        history[user] = []
    
    history[user].append(password)
    
    history[user] = history[user][-10:]  # Keep only last 10
    
    save_password_history(history)



def blackListPass():
    try:
        with open("common_passwords.txt", "r") as myFile:  # Auto-closes file
            dataList = {line.strip() for line in myFile}  # Convert to Set & Remove \n
        return dataList
    except FileNotFoundError:
        return set()  # Agar file nahi mili to empty set return karega

def suggestPass():
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
    password = ''.join(secrets.choice(alphabet) for i in range(12))
    # all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"

    # password = ''.join(random.choice(all_chars) for _ in range(12))
    return password

def score_checker(score):
    if score <= 2:
        st.warning(f"🔴 Weak Password (Score: {score}/5)")
    elif score >= 3 and score <= 4:
        st.info(f"🟠 Moderate Password (Score: {score}/5)")
    else:
        st.success(f"🟢 Strong Password (Score: {score}/5)")

def passswor_checker(password):
    score = 0
    feedbacks = []
    if len(password) < 8:
        feedbacks.append("Password Should be atleast 8 character long")
        
    else:
        score += 1

    if not re.search(r"[A-Z]",password) or not re.search(r"[a-z]",password):
        feedbacks.append("Password Should contain atleast one upper case and one lower case letter")
        
    else:
        score += 1

    # The pattern \d matches any digit (0-9)
    if not re.search(r"\d",password):
        feedbacks.append("Password Should contain atleast one digit")
        
    else:
        score += 1

    # The pattern matches special chareacter in string
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",password):
        feedbacks.append("Password Should contain atleast one special character")
        
    else:
        score += 1

    if len(password) >= 12:
        score += 1
    else:
        feedbacks.append("Use 12+ characters for better security") 

    if feedbacks:
            st.error("Improve Passowrd by adding:\n\n" + "\n\n".join(feedbacks))

    score_checker(score)
def main():
    st.title("Password Strength Meter")
    password = st.text_input("Enter Your Password",value=st.session_state.get('generated_pass'))
    user_id = get_user()
    if st.button("Check Password"):
        if password:
            if password in blackListPass():
                st.error("⚠️ Weak Password! Choose a stronger one") 
            else:
                if is_reused_password(user_id, password):
                    st.error("🚨 This password was used before! Choose a new one.")
                else:
                    update_password_history(user_id, password)
                    passswor_checker(password)
        else:
            
            st.error("Please enter a password.")

    if st.button("Suggest Strong password"):
        st.session_state.generated_pass = suggestPass()
        # print(password)
        st.rerun()
if __name__ == "__main__":
    main()
