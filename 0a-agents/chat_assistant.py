
import json

from IPython.display import display, HTML
import markdown

class Tools:
    def __init__(self):
        self.tools = {}
        self.functions = {}

    def add_tool(self, function, description):
        self.tools[function.__name__] = description
        self.functions[function.__name__] = function
    
    def get_tools(self):
        return list(self.tools.values())

    def function_call(self, tool_call):
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        f = self.functions[function_name]
        result = f(**arguments)

        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": json.dumps(result, indent=2),
        }


def shorten(text, max_length=50):
    if len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."


class ChatInterface:
    def input(self):
        question = input("You:")
        return question
    
    def display(self, message):
        print(message)

    def display_function_call(self, entry, result):
        call_html = f"""
            <details>
            <summary>Function call: <tt>{entry.function.name}({shorten(entry.function.arguments)})</tt></summary>
            <div>
                <b>Call</b>
                <pre>{entry}</pre>
            </div>
            <div>
                <b>Output</b>
                <pre>{result['content']}</pre>
            </div>
            
            </details>
        """
        display(HTML(call_html))

    def display_response(self, entry):
        response_html = markdown.markdown(entry.message.content)
        html = f"""
            <div>
                <div><b>Assistant:</b></div>
                <div>{response_html}</div>
            </div>
        """
        display(HTML(html))



class ChatAssistant:
    def __init__(self, tools, developer_prompt, chat_interface, client, model):
        self.tools = tools
        self.developer_prompt = developer_prompt
        self.chat_interface = chat_interface
        self.client = client
        self.model = model
    
    def gpt(self, chat_messages):
        return self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=chat_messages,
            tools=self.tools.get_tools(),
            tool_choice="auto",
        )


    def run(self):
        chat_messages = [
            {"role": "system", "content": self.developer_prompt},
        ]

        # Chat loop
        while True:
            question = self.chat_interface.input()
            if question.strip().lower() == 'stop':  
                self.chat_interface.display("Chat ended.")
                break

            message = {"role": "user", "content": question}
            chat_messages.append(message)

            while True:  # inner request loop
                response = self.gpt(chat_messages)

                has_messages = False

                for entry in response.choices:
                    chat_messages.append(entry.message)

                    if entry.finish_reason == "tool_calls":
                        for tool_call in entry.message.tool_calls:
                            result = self.tools.function_call(tool_call)
                            chat_messages.append(result)
                            self.chat_interface.display_function_call(tool_call, result)

                    elif entry.finish_reason == "stop":
                        self.chat_interface.display_response(entry)
                        has_messages = True

                if has_messages:
                    break
    
