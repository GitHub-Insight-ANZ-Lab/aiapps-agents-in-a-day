const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

// TODO: Replace with your Azure OpenAI endpoint and key
const client = new OpenAIClient(
  "https://<AZURE_OPENAI_API_INSTANCE_NAME>.openai.azure.com/",
  new AzureKeyCredential("<AZURE_OPENAI_API_KEY>")
);

// Define the function that the model can call
const searchBikeStore = {
  name: "search_bike",
  description: "Retrieves bikes from the search index based on location, company, and model",
  parameters: {
    type: "object",
    properties: {
      location: {
        type: "string",
        description: "The location of the store (i.e. Seattle, WA)",
      },
      company: {
        type: "string",
        description: "The company of the bike",
      },
      model: {
        type: "string",
        description: "The model of the bike",
      },
    },
    required: ["location"],
  },
};

const options = {
  tools: [
    {
      type: "function",
      function: searchBikeStore,
    },
  ],
};

// Chat completion with function calling
const chatResponse = client.getChatCompletions("completions", [
  {
    role: "system",
    content:
      "You are a helpful, fun and friendly sales assistant for Contoso Bike Store, a bicycle and bicycle accessories store.",
  },
  {
    role: "user",
    content:
      "I'm looking for a bike in Seattle store. Can you help me find a bike from Trek company and model Domane SLR 9?",
  },
], options);

// Function to handle tool call responses
function applyToolCall({ function: call, id }) {
  if (call.name === "search_bike") {
    console.log('[applyToolCall] invoked');
    const { location, company, model } = JSON.parse(call.arguments);
    // In a real application, this would be a call to an external service or database.
    return {
      role: "tool",
      content: `The bike from ${company} company and model ${model} is available in ${location} store.`,
      toolCallId: id,
    };
  }
  throw new Error(`Unknown tool call: ${call.name}`);
}

// Handle the response and tool calls
chatResponse
  .then(async (result) => {
    console.log('[chatResponse]:', JSON.stringify(result, null, 2));
    console.log('');
    console.log('[chatResponse][Message]:', JSON.stringify(result.choices[0].message, null, 2));
    console.log('');

    for (const choice of result.choices) {
      const responseMessage = choice.message;

      if (responseMessage?.role === "assistant") {
        const requestedToolCalls = responseMessage?.toolCalls;
        if (requestedToolCalls?.length) {
          const toolCallResolutionMessages = [
            responseMessage,
            ...requestedToolCalls.map(applyToolCall),
          ];

          console.log('[toolCallResolutionMessages]:', JSON.stringify(toolCallResolutionMessages, null, 2));
          console.log('');

          const finalResult = await client.getChatCompletions('completions', toolCallResolutionMessages);
          console.log('[chatResponse_with_toolcall]:', JSON.stringify(finalResult, null, 2));
          console.log('');
          console.log('[Final Response]:', finalResult.choices[0].message.content);
        }
      }
    }
  })
  .catch((err) => console.log(`Error: ${JSON.stringify(err)}`));