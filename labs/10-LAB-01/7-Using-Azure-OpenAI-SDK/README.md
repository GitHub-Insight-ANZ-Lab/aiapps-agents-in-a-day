# Azure OpenAI SDK Lab

This directory contains practical examples for using the Azure OpenAI SDK with Node.js.

:::warning Package Notice
This lab uses `@azure/openai@1.0.0-beta.11` which is deprecated. For production applications, migrate to the stable OpenAI SDK. This lab serves educational purposes and demonstrates the concepts which apply to the newer SDK as well.
:::

## Setup Instructions

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure your credentials:**
   - Copy `config-template.js` to `config.js`
   - Replace the placeholder values with your actual Azure OpenAI credentials

3. **Run the examples:**
   ```bash
   # Basic completion example
   npm run basic
   
   # System message example
   npm run system
   
   # Conversation history example
   npm run conversation
   
   # Function calling example
   npm run function
   ```

## File Descriptions

- `01-basic-completion.js` - Basic chat completion
- `02-system-message.js` - Using system messages to set behavior
- `03-conversation-history.js` - Maintaining conversation context
- `04-function-calling.js` - Advanced function calling with tools
- `config-template.js` - Template for Azure OpenAI configuration

## Alternative: Manual Configuration

If you prefer not to use the config file, you can directly edit the endpoint and API key in each JavaScript file where you see:
```javascript
const client = new OpenAIClient(
  "https://<AZURE_OPENAI_API_INSTANCE_NAME>.openai.azure.com/",
  new AzureKeyCredential("<AZURE_OPENAI_API_KEY>")
);
```