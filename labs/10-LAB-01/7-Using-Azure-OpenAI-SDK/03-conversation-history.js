const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

// TODO: Replace with your Azure OpenAI endpoint and key
const client = new OpenAIClient(
  "https://<AZURE_OPENAI_API_INSTANCE_NAME>.openai.azure.com/",
  new AzureKeyCredential("<AZURE_OPENAI_API_KEY>")
);

// Chat completion with conversation history
const chatResponse = client.getChatCompletions("completions", [
  {
    role: "system",
    content:
      "You are a helpful, fun and friendly sales assistant for Contoso Bike Store, a bicycle and bicycle accessories store.",
  },
  { role: "user", content: "Do you sell bicycles?" },
  {
    role: "assistant",
    content:
      "Yes, we do sell bicycles. What kind of bicycle are you looking for?",
  },
  {
    role: "user",
    content: "I'm not sure what I'm looking for. Could you help me decide?",
  },
]);

// Print the response from Azure OpenAI to the console
chatResponse
  .then((result) => {
    for (const choice of result.choices) {
      console.log(choice.message.content);
    }
  })
  .catch((err) => console.log(`Error: ${JSON.stringify(err)}`));