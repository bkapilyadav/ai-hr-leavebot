import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

st.set_page_config(page_title="LeaveBot AI", page_icon="🧠")
st.title("🧠 AI LeaveBot – HR Automation Assistant")

employee_name = st.text_input("Enter your full name")
leave_request = st.text_area("Describe your leave request")

# Load employee data
df = pd.read_csv("employee_data.csv")

# Load the vector store
vectordb = Chroma(persist_directory="policy_db", embedding_function=OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=vectordb.as_retriever())

if st.button("Submit Request"):
    emp_data = df[df['name'].str.lower() == employee_name.lower()]

    if emp_data.empty:
        st.error("❌ Employee not found. Check the name.")
    else:
        leave_balance = int(emp_data.iloc[0]['leave_balance'])
        st.markdown(f"📊 **Current Leave Balance**: `{leave_balance}` days")

        # Run AI over policy
        policy_response = qa_chain.run(leave_request)

        result = f"🧠 *AI Response:*\n{policy_response}\n\n✅ You have {leave_balance} days left."
        st.success(result)

        with open("logs.csv", "a") as f:
            f.write(f"{employee_name},{leave_request},{result}\n")
