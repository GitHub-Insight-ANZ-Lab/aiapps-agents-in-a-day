# Using Azure OpenAI SDK

:::tip Azure OpenAI SDK
Azure OpenAI SDK is a set of libraries that allow you to interact with Azure OpenAI services from your code. The SDK are available for multiple programming languages, including Python, Node.js, and C#.
:::

In this lab, you will learn how to use the Azure OpenAI SDK to interact with Azure OpenAI services from your code using Node.js. We've prepared ready-to-run examples that you can execute and modify.

## Quick Start

1. Open a new `Terminal` window in VS code and navigate to the lab directory:

```bash
cd labs/10-LAB-01/7-Using-Azure-OpenAI-SDK
```

2. Install the dependencies:

```bash
npm install
```

:::warning Package Version
The `@azure/openai` package used in this lab is a beta version. For production applications, consider using the stable OpenAI SDK with Azure OpenAI support. This lab uses the beta version for educational purposes.
:::

3. **Configure your Azure OpenAI credentials:**
   - Copy `config-template.js` to `config.js` and update with your credentials, OR
   - Edit the endpoint and API key directly in each JavaScript file

:::info
Azure OpenAI service endpoint is in the format `https://<AZURE_OPENAI_API_INSTANCE_NAME>.openai.azure.com/`. 
If unsure about your instance name, refer to the `Lab Setup` documentation.
:::

4. **Run the basic example:**

```bash
npm run basic
# or alternatively: node 01-basic-completion.js
```

You should see a response from the Azure OpenAI service about different types of road bikes.

:::info
More information on the Azure OpenAI client methods can be found in the [@azure/openai package](https://learn.microsoft.com/en-us/javascript/api/%40azure/openai/?view=azure-node-preview) documentation. 
:::

## Example 1: Basic Chat Completion

The `01-basic-completion.js` file demonstrates a simple chat completion:

```bash
npm run basic
```

This example shows how to:
- Import the Azure OpenAI client
- Create a client instance with your credentials
- Send a basic user message
- Process and display the response

## Example 2: System Message

The `02-system-message.js` file demonstrates how to use system messages to set the AI's behavior and personality:

```bash
npm run system
```

This example shows how to:
- Set a system message to define the AI's role
- Create a more conversational and contextual response
- Guide the AI to behave as a specific type of assistant

**Key concept:** System messages help establish the AI's persona and instructions before the conversation begins.

## Example 3: Conversation History

The `03-conversation-history.js` file demonstrates how to maintain context across multiple turns:

```bash
npm run conversation
```

This example shows how to:
- Include previous messages in the conversation
- Build context over multiple exchanges
- Create more natural, flowing conversations

**Key concept:** LLMs are stateless, so you must explicitly provide conversation history to maintain context.

## Example 4: Function Calling

The `04-function-calling.js` file demonstrates advanced function calling capabilities:

```bash
npm run function
```

This example shows how to:
- Define functions that the AI can call
- Handle tool responses
- Create interactive applications where the AI can perform actions

**Key concept:** Function calling allows the AI to use external tools and services, extending its capabilities beyond text generation.

:::tip
Where do you think the actual `applyToolCall` execution happens? On the server-side or client-side?

Answer: Client-side! The AI decides when to call a function and what parameters to use, but the actual function execution happens in your application code.
:::

## Understanding the Code Structure

All the example files follow a similar pattern:

1. **Import and Setup**: Import the Azure OpenAI client and create an instance
2. **Define the Request**: Set up the messages and any options (like function definitions)
3. **Make the API Call**: Send the request to Azure OpenAI
4. **Handle the Response**: Process the result and display or use the output

You can modify any of the examples to experiment with different:
- System messages and personas
- User prompts and questions
- Function definitions and responses
- Error handling approaches

## Next Steps

Try modifying the examples:
- Change the system messages to create different AI personas
- Add your own functions to the function calling example
- Experiment with different conversation flows
- Add error handling and validation
