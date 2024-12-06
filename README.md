# ℹ️ About

This innovative chatbot is designed to help you interact effortlessly with your SQLite database using the power of advanced AI and human collaboration. Whether you're a database expert or just getting started, this tool provides an intuitive way to query and manage data with precision.

### Key Features:

- **Natural Language Querying**: Simply describe the information you’re looking for in plain language, and the chatbot will generate an appropriate SQL query for you.
- **Human-in-the-Loop**: Review and modify the generated SQL query before execution. This ensures you retain full control over your data and enhances transparency in the querying process.
- **Instant Results**: Execute the query to retrieve your data instantly, streamlining your workflow and saving time.
- **Learn SQL On-the-Go**: By reviewing and tweaking the generated queries, you can improve your understanding of SQL in a hands-on and practical manner.

<!-- --- -->

<!-- ### <a href="https://finance-chatbot-vincent-cheng.streamlit.app/" target="_blank">Check SharePoint Chatbot/RAG Live</a> -->

---

## How It Works

1. **Ask a Question:** Type your request in natural language (e.g., _"Show me NVDA monthly average volumes in 2024"_).
2. **Review the SQL Query:** The chatbot will generate an SQL query based on your input. You can review and modify it as needed.
3. **Run the Query:** Once you're satisfied with the query, execute it to see the results.

---

### Tech Stack:

- Frontend:
  - Streamlit
- Backend:
  - Search/Vector Retrieval: LangChain
  - Database: SQLite (local)
- Search/Retrieval Layer:
  - Database: SQLite (local)
  - Pretrained Models:
    - OpenAI's Model API (gpt-4o-mini)
- Cloud Services:
  - Deployment: Streamlit Community Cloud

---

### Workflow in the RAG Pipeline:

#### Answer User Query

1. Query generation:

   - Generate SQL query based on user question.
   - Human to review the query and provide modified query if required.

2. Query execution:

   - Execute SQL query on the database to retrieve result.

3. Answer Generation:

   - Generate answer based on retrieved result.

4. Response Delivery:
   - Present results in the frontend.

---

Developed by Vincent Cheng  
<a href="https://www.linkedin.com/in/yun-sheng-cheng-86094a143/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="height:30px; width:30px;filter: grayscale(100%);">
</a>
