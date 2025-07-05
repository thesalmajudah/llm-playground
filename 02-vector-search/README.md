# 🔍 Module 2 – Vector Search in RAG Systems

![Module 2 Overview](images/module2.jpeg)

Module 2 delivered a powerful deep dive into **Vector Search**, one of the foundational building blocks of modern Retrieval-Augmented Generation (RAG) systems.

## 💡 Key Takeaways

- **Vector databases**: Deployed and explored Qdrant locally via Docker, enjoying its Web UI for hands-on semantic indexing and retrieval.
- **Text embeddings**: Generated numeric representations of text using `BAAI/bge-small-en` and `FastEmbed`.
- **Semantic vs. text search**: Transitioned from keyword-based methods to true semantic matching using cosine similarity.
- **Dense vs. sparse vectors**: Learned the difference between dense (neural embeddings, like sentence transformers) and sparse (term-based, like TF-IDF/BM25) representations — and when to use each.
- **Hybrid search**: Combined vector and term-based queries to balance precision and recall, following proven RAG best practices.

## ⚙️ Vector Search Pipeline

1. **Embed** FAQ documents
2. **Index** them in Qdrant
3. **Embed** user queries
4. **Retrieve** top-k semantically similar documents
5. **Build** prompts with context
6. **Query** LLM → generate grounded responses

## 🧪 Big Idea

Vector search empowers LLMs to surface relevant, context-rich information — significantly enhancing answer accuracy and user experience.
