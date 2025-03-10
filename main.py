import re
import streamlit as st
import string
import secrets
import random

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
    
    if st.button("Check Password"):
        if password:
            if password in blackListPass():
                st.error("⚠️ Weak Password! Choose a stronger one") 
            else:
                passswor_checker(password)
        else:
            
            st.error("Please enter a password.")

    if st.button("Suggest Strong password"):
        st.session_state.generated_pass = suggestPass()
        # print(password)
        st.rerun()
if __name__ == "__main__":
    main()
