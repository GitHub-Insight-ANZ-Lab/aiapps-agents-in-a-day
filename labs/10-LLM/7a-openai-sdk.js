const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

const client = new OpenAIClient(
  "https://aiaaa-s2-openai.openai.azure.com/",
  new AzureKeyCredential("<YOUR_AZURE_OPENAI_KEY_HERE>")
);

// Block Reference 1
const chatResponse = client.getChatCompletions("gpt-4o", [
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

// Block Reference 2
chatResponse
  .then((result) => {
    for (const choice of result.choices) {
      console.log(choice.message.content);
    }
  })
  .catch((err) => console.log(`Error: ${JSON.stringify(err)}`));