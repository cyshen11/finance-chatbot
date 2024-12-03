"""Settings page"""

import streamlit as st
from components.database import create_database, test_database
import os

admin_acc = st.secrets["SQL_ADMIN"]

st.title("⚙️ Settings")

user_name = st.text_input("User Name")
password = st.text_input("Password", type="password")

if user_name == admin_acc["USERNAME"] and password == admin_acc["PASSWORD"]:
    create_db = st.button("Create Database")
    test_db = st.button("Test Database")
    if create_db:
        try:
          create_database()
          st.success("✅ Database created successfully!")
        except:
          st.error("❌ Database creation fail.")
    if test_db:
    #   try:
      query_result = test_database()
      st.dataframe(query_result)
        #   except:
        #     st.error("❌ Database test fail.")
        
else:
    st.error("❌ Invalid user name or password.")