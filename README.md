# ℹ️ About

This chatbot, powered by Retrieval-Augmented Generation (RAG) technology, enables users to seamlessly query and retrieve information from PDF documents stored in Microsoft SharePoint. It combines the capabilities of AI-driven natural language understanding and advanced search algorithms to provide precise and context-aware answers.

### Key Features:

- **Natural Language Queries**: Users can ask questions in plain language, and the chatbot understands the intent to fetch relevant information.
- **PDF Parsing**: Extracts and interprets text, tables, and key details from PDFs with high accuracy.
- **SharePoint Integration**: Directly accesses and searches through SharePoint repositories without manual downloads or organization.
- **Real-Time Insights**: Provides immediate, contextually relevant responses drawn from the most pertinent sections of the documents.

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

### <a href="https://finance-chatbot-vincent-cheng.streamlit.app/" target="_blank">Check SharePoint Chatbot/RAG Live</a>

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

   - Combine retrieved snippets with OpenAI's model(gpt-4o-mini) to generate a response.

3. Response Delivery:
   - Present results in the frontend.
