# 🧪 Module 3 – Evaluation 

> Explores how to evaluate and monitor Retrieval-Augmented Generation (RAG) pipelines using classical metrics, LLM-as-a-judge, and monitoring tools.

---

![Evaluation Preview](image.webp)

---

## 📌 Highlights

### 🔍 Offline Evaluation
Evaluate system performance using metrics:
- **Hit Rate** – Did any correct document appear in top-k?
- **MRR (Mean Reciprocal Rank)** – How early is the correct document ranked?
- **Precision@k** – Proportion of relevant results in top-k.
- **Cosine Similarity** – Vector-based similarity for embeddings.

### 🤖 LLM-as-a-Judge
Use LLMs like `gpt-4o` or `llama3-70b` to:
- Compare generated answers to reference ones.
- Score relevance, helpfulness, correctness.
- Run zero-shot or few-shot evaluations.

### 📋 Ground Truth Generation
Use LLMs to auto-generate:
- Questions
- Reference answers
- Relevance judgments for evaluating retrieval

---

## 🔧 Tools & Stack
- `OpenAI GPT-4o` & `Groq LLaMA3`
- `Qdrant` for vector search
- `Sentence-Transformers` (for embedding model)
- `Matplotlib` / `Pandas` for visualization
- `Jupyter` notebooks

---
