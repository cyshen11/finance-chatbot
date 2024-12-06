# ℹ️ About

This innovative chatbot is designed to help you interact effortlessly with your SQLite database using the power of advanced AI and human collaboration. Whether you're a database expert or just getting started, this tool provides an intuitive way to query and manage data with precision.

### Key Features:

- **Natural Language Querying**: Simply describe the information you’re looking for in plain language, and the chatbot will generate an appropriate SQL query for you.
- **Human-in-the-Loop**: Review and modify the generated SQL query before execution. This ensures you retain full control over your data and enhances transparency in the querying process.
- **Instant Results**: Execute the query to retrieve your data instantly, streamlining your workflow and saving time.
- **Learn SQL On-the-Go**: By reviewing and tweaking the generated queries, you can improve your understanding of SQL in a hands-on and practical manner.

---

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
  - Document Processing: PyMuPDF
  - Search/Vector Retrieval: LangChain
  - Database/Embedding Store: ChromaDB (local)
- Search/Retrieval Layer:
  - Vector Database: ChromaDB (local)
  - Pretrained Models:
    - OpenAI's Embeddings API (text-embedding-3-large)
    - OpenAI's Model API (gpt-4o-mini)
    - Google's Embeddings API (embedding-001)
    - Google's Model API (gemini-1.5-flash-8b)
- Cloud Services:
  - Storage: Microsoft SharePoint
  - Deployment: Streamlit Community Cloud

---

### Workflow in the RAG Pipeline:

#### Create vector database

1. Document Ingestion:

   - Upload documents from SharePoint.
   - Load documents from Sharepoint using Langchain SharePoint Loader.

2. Embedding Generation:

   - Initialize ChromaDB with specified embeddings function.

3. Embedding Storage:
   - Store the documents in ChromaDB.

#### Answer User Query

1. Query Processing:

   - User input is embedded and matched against stored embeddings.
   - Retrieve relevant documents.

2. Answer Generation:

   - Combine retrieved snippets with LLM model to generate a response.

3. Response Delivery:
   - Present results in the frontend.

---

Developed by Vincent Cheng  
<a href="https://www.linkedin.com/in/yun-sheng-cheng-86094a143/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="height:30px; width:30px;filter: grayscale(100%);">
</a>
