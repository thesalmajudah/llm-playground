import json
from IPython.display import display, HTML
import markdown


class Tools:
    def __init__(self):
        self.functions = {}     # function name -> callable
        self.tool_specs = []    # list of OpenAI/Groq-compatible function specs

    def add_tool(self, function, function_spec):
        """Add a callable tool with its full OpenAI-style spec."""
        tool_name = function_spec["function"]["name"]
        self.functions[tool_name] = function

        # Ensure correct structure: {"type": "function", "function": {...}}
        self.tool_specs.append({
            "type": "function",
            "function": function_spec["function"]
        })

    def get_tools(self):
        return self.tool_specs

    def function_call(self, tool_call_response):
        # Access name and arguments from Groq's structured tool call
        function_name = tool_call_response.function.name
        arguments = json.loads(tool_call_response.function.arguments)

        f = self.functions[function_name]
        result = f(**arguments)

        return {
            "type": "function_call_output",
            "call_id": tool_call_response.id,
            "output": json.dumps(result, indent=2)
        }


def shorten(text, max_length=50):
    return text if len(text) <= max_length else text[:max_length - 3] + "..."


class ChatInterface:
    def input(self):
        return input("You: ")

    def display(self, message):
        print(message)

    def display_function_call(self, entry, result):
        call_html = f"""
        <details>
        <summary>Function call: <tt>{entry.function.name}({shorten(entry.function.arguments)})</tt></summary>
        <div>
            <b>Call</b>
            <pre>{json.dumps(entry.model_dump(), indent=2)}</pre>
        </div>
        <div>
            <b>Output</b>
            <pre>{result['output']}</pre>
        </div>
        </details>
        """
        display(HTML(call_html))

    def display_response(self, entry):
        display(HTML(f"<div><b>Assistant:</b><br>{markdown.markdown(entry.content)}</div>"))


class ChatAssistant:
    def __init__(self, tools, developer_prompt, chat_interface, client):
        self.tools = tools
        self.developer_prompt = developer_prompt
        self.chat_interface = chat_interface
        self.client = client

    def gpt(self, chat_messages):
        return self.client.chat.completions.create(
            model="llama3-70b-8192",  # or another Groq-compatible model
            messages=chat_messages,
            tools=self.tools.get_tools(),
            tool_choice="auto"
        )

    def run(self):
        chat_messages = [
            {"role": "system", "content": self.developer_prompt}
        ]

        while True:
            question = self.chat_interface.input()
            if question.strip().lower() == "stop":
                self.chat_interface.display("Chat ended.")
                break

            chat_messages.append({"role": "user", "content": question})
            max_depth = 5
            depth = 0

            while depth < max_depth:
                response = self.gpt(chat_messages)
                message = response.choices[0].message

                # Handle tool calls
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        result = self.tools.function_call(tool_call)

                        chat_messages.append({
                            "role": "assistant",
                            "content": None,
                            "function_call": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        })

                        chat_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result["output"]
                        })

                        self.chat_interface.display_function_call(tool_call, result)

                # Handle assistant message
                if message.content:
                    chat_messages.append({
                        "role": "assistant",
                        "content": message.content
                    })
                    self.chat_interface.display_response(message)
                    break

                depth += 1
            else:
                self.chat_interface.display("⚠️ Reached tool recursion limit without assistant reply.")
