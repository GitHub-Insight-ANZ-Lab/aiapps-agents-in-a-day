const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

// TODO: Replace with your Azure OpenAI endpoint and key
const client = new OpenAIClient(
  "https://<AZURE_OPENAI_API_INSTANCE_NAME>.openai.azure.com/",
  new AzureKeyCredential("<AZURE_OPENAI_API_KEY>")
);

// Basic chat completion example
const chatResponse = client.getChatCompletions("completions", [
  { role: "user", content: "What are the different types of road bikes?" },
]);

// Print the response from Azure OpenAI to the console
chatResponse
  .then((result) => {
    for (const choice of result.choices) {
      console.log(choice.message.content);
    }
  })
  .catch((err) => console.log(`Error: ${JSON.stringify(err)}`));