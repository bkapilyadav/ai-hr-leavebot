import os
import streamlit as st
import pandas as pd
import openai

# Set OpenAI API key
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except Exception as e:
    st.error("Error accessing API key. Please add OPENAI_API_KEY to your app secrets.")
    st.stop()

st.set_page_config(page_title="LeaveBot AI", page_icon="🧠")
st.title("🧠 AI LeaveBot – HR Automation Assistant")

# Rest of your code...

employee_name = st.text_input("Enter your full name")
leave_request = st.text_area("Describe your leave request")

# Sample leave policy text - in a real app, you'd load this from a file
LEAVE_POLICY = '''
Company Leave Policy:
1. Employees are entitled to 20 days of annual leave per year.
2. Sick leave requires a doctor's note for absences longer than 2 days.
3. Parental leave is 12 weeks for primary caregivers and 4 weeks for secondary caregivers.
4. Leave requests must be submitted at least 7 days in advance for planned absences.
5. Emergency leave can be granted with manager's approval.
'''

# Load employee data - create a sample if file doesn't exist
try:
    df = pd.read_csv("employee_data.csv")
except:
    # Create sample data
    df = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith', 'Test User'],
        'leave_balance': [15, 18, 10]
    })
    df.to_csv("employee_data.csv", index=False)
    st.info("Created sample employee data file")

if st.button("Submit Request"):
    emp_data = df[df['name'].str.lower() == employee_name.lower()]

    if emp_data.empty:
        st.error("❌ Employee not found. Check the name.")
    else:
        leave_balance = int(emp_data.iloc[0]['leave_balance'])
        st.markdown(f"📊 **Current Leave Balance**: `{leave_balance}` days")

        # Use OpenAI directly instead of a vector database
        prompt = f'''
        Based on the following leave policy:
        {LEAVE_POLICY}

        And considering that {employee_name} has {leave_balance} days of leave balance,
        analyze this leave request: "{leave_request}"

        Provide a brief response about whether this request complies with policy,
        any special considerations, and next steps.
        '''

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are an HR assistant that helps with leave requests."},
        {"role": "user", "content": prompt}
                    ]
                    )

        policy_response = response.choices[0].message.content

        result = f"🧠 *AI Response:*\n{policy_response}\n\n✅ You have {leave_balance} days left."
        st.success(result)

        # Log the request
        try:
            with open("logs.csv", "a") as f:
                f.write(f"{employee_name},{leave_request},{policy_response}\n")
        except:
            with open("logs.csv", "w") as f:
                f.write("employee,request,response\n")
                f.write(f"{employee_name},{leave_request},{policy_response}\n")
