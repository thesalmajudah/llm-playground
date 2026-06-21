INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT:
{context}
""".strip()

class RAGBase:

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        course="llm-zoomcamp",
        model="llama-3.1-8b-instant"
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    # The search method delegates to the index

    def search(self, query, num_results=5):
        boost_dict = {"question": 3.0, "section": 0.5}
        filter_dict = {"course": self.course}

        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict
        )
    
    # The build_context and build_prompt methods format the search results

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append(doc["section"])
            lines.append("Q: " + doc["question"])
            lines.append("A: " + doc["answer"])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )
    
    # The llm method sends the prompt to the LLM

    def llm(self, prompt):
        # OpenAI-compatible clients (including Groq)
        if hasattr(self.llm_client, "chat") and hasattr(self.llm_client.chat, "completions"):
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content

        # Gemini-style clients
        if hasattr(self.llm_client, "models") and hasattr(self.llm_client.models, "generate_content"):
            response = self.llm_client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={"system_instruction": self.instructions},
            )
            return response.text

        raise TypeError("Unsupported llm_client interface. Expected OpenAI-compatible or Gemini-style client.")
    
    # And the rag method wires it all together
    
    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm(prompt)
        return answer