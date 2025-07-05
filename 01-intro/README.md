# 🧠 Module 1 – Retrieval-Augmented Generation (RAG)

![Module 1 Overview](images/module1.jpeg)

In Module 1, I built a basic RAG (Retrieval-Augmented Generation) flow that searches a knowledge base and retrieves relevant context to improve LLM responses.

## 🔑 Key Takeaways

- **Core concepts**: Solidified my understanding of LLMs and RAG.
- **Hands-on setup**: Used the Groq API and Elasticsearch to implement RAG search.
- **Search mechanics**: Indexed FAQ documents and boosted queries for better retrieval.

## ⚙️ RAG Architecture

1. **Query**: Accept a user question.
2. **Retrieve**: Fetch relevant documents from Elasticsearch.
3. **Build Prompt**: Dynamically construct a prompt with retrieved context.
4. **LLM Response**: Send the prompt to an LLM and generate an answer.
