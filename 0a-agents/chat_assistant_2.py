import json
import inspect
import markdown
from IPython.display import display, HTML

from groq import Groq


def shorten(text, max_length=50):
    if len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."


def generate_description(function):
    """
    Generate a tool description schema for a given function using its docstring and signature.
    """

    # Get function name and docstring
    name = function.__name__
    doc = inspect.getdoc(function) or "No description provided."

    # Get function signature
    sig = inspect.signature(function)
    properties = {}
    required = []

    for param in sig.parameters.values():
        param_name = param.name
        param_type = param.annotation if param.annotation != inspect._empty else str

        # Map Python types to JSON schema types
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            dict: "object",
            list: "array"
        }
        json_type = type_map.get(param_type, "string")  # default to string

        properties[param_name] = {
            "type": json_type,
            "description": f"{param_name} parameter"
        }

        # Consider all parameters required unless they have a default
        if param.default == inspect._empty:
            required.append(param_name)

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": doc,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False
            }
        }
    }


class Tools:

    def __init__(self):
        self.tools = {}
        self.functions = {}
    
    def add_tool(self, function, description=None):
        if description is None:
            description = generate_description(function)
        self.tools[function.__name__] = description
        self.functions[function.__name__] = function

    def add_tools(self, instance):
        for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
            if not name.startswith("_"):  # skip private and special methods
                self.add_tool(method)
    
    def get_tools(self):
        return list(self.tools.values())

    def function_call(self, tool_call):
        args = json.loads(tool_call.function.arguments)
        f_name = tool_call.function.name
        f = self.functions[f_name]
        
        results = f(**args)
        
        return {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": f_name,
            "content": json.dumps(results)
        }


class IPythonChatInterface:

    def input(self):
        question = input('User: ').strip()
        return question

    def display(self, content):
        print(content)

    def display_function_call(self, name, arguments, output):
        short_arguments = shorten(arguments)

        call_html = f"""
            <details>
                <summary>Function call: <tt>{name}({short_arguments})</tt></summary>
                <div>
                    <b>Call</b>
                    <pre>{arguments}</pre>
                </div>
                <div>
                    <b>Output</b>
                    <pre>{output}</pre>
                </div>
            </details>
        """
        display(HTML(call_html))

    def display_response(self, md_content):
        html_content = markdown.markdown(md_content)

        html = f"""
            <div>
                <div><b>Assistant:</b></div>
                <div>{html_content}</div>
            </div>
        """
        display(HTML(html))


class ChatAssistant:

    def __init__(self, tools: Tools, developer_prompt: str, interface: IPythonChatInterface, groq_client: Groq):
        self.tools = tools
        self.developer_prompt = developer_prompt
        self.interface = interface
        self.groq_client = groq_client

    def run(self) -> None:
        chat_messages = [
            {"role": "system", "content": self.developer_prompt},
        ]
        
        while True: # Q&A loop
            question = self.interface.input()
        
            if question.lower() == 'stop':
                self.interface.display('Chat ended')
                break
        
            chat_messages.append({"role": "user", "content": question})
        
            while True:
                response = self.groq_client.chat.completions.create(
                    model='llama3-70b-8192',
                    messages=chat_messages,
                    tools=self.tools.get_tools(),
                    tool_choice="auto"
                )
        
                message = response.choices[0].message
                chat_messages.append(message)
                
                # Display assistant response if there's content
                if message.content:
                    self.interface.display_response(message.content)
                
                # Handle tool calls
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        # Execute the function call
                        tool_response = self.tools.function_call(tool_call)
                        
                        # Display the function call
                        self.interface.display_function_call(
                            tool_call.function.name,
                            tool_call.function.arguments,
                            tool_response["content"]
                        )
                        
                        # Add tool response to chat history
                        chat_messages.append(tool_response)
                    
                    # Continue the loop to get the final response
                    continue
                else:
                    # No tool calls, we're done with this turn
                    break

