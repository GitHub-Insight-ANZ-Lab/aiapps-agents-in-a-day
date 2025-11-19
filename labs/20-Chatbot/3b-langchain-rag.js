require('dotenv').config();
const { MongoClient } = require('mongodb');
const { OpenAIEmbeddings, ChatOpenAI } = require("@langchain/openai");
// To support the LangChain LCEL RAG chain
const { PromptTemplate } = require("@langchain/core/prompts");
const {
    RunnableSequence,
    RunnablePassthrough,
} = require("@langchain/core/runnables");
const { StringOutputParser } = require("@langchain/core/output_parsers");

const { AzureCosmosDBVectorStore,
    AzureCosmosDBSimilarityType
} = require("@langchain/community/vectorstores/azure_cosmosdb")


// set up the MongoDB client
const dbClient = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
var dbname = process.env.MONGODB_Name;

// set up the Azure Cosmos DB vector store using the initialized MongoDB client
const azureCosmosDBConfig = {
    client: dbClient,
    databaseName: dbname,
    collectionName: "products",
    indexName: "VectorSearchIndex",
    embeddingKey: "contentVector",
    textKey: "_id"
}
const vectorStore = new AzureCosmosDBVectorStore(new OpenAIEmbeddings(), azureCosmosDBConfig);
// set up the OpenAI chat model
const chatModel = new ChatOpenAI();

async function main() {
    try {
        await dbClient.connect();
        console.log("Connected to MongoDB");
        // Test the RAG chain
        console.log(await ragLCELChain("What is the name of the product that has the SKU TI-R982?"));

    } catch (err) {
        console.error(err);
    } finally {
        await dbClient.close();
        console.log('Disconnected from MongoDB');
    }
}

function formatDocuments(docs) {
  // Prepares the product list for the system prompt.
  let strDocs = "";
  for (let index = 0; index < docs.length; index++) {
    let doc = docs[index];
    let docFormatted = { _id: doc.pageContent };
    Object.assign(docFormatted, doc.metadata);

    // Build the product document without the contentVector and tags
    if ("contentVector" in docFormatted) {
      delete docFormatted["contentVector"];
    }
    if ("tags" in docFormatted) {
      delete docFormatted["tags"];
    }

    // Add the formatted product document to the list
    strDocs += JSON.stringify(docFormatted, null, "\t");

    // Add a comma and newline after each item except the last
    if (index < docs.length - 1) {
      strDocs += ",\n";
    }
  }
  // Add two newlines after the last item
  strDocs += "\n\n";
  return strDocs;
}

async function ragLCELChain(question) {
  // A system prompt describes the responsibilities, instructions, and persona of the AI.
  // Note the addition of the templated variable/placeholder for the list of products and the incoming question.
  const systemPrompt = `
        You are a helpful, fun and friendly sales assistant for Contoso Bike Store, a bicycle and bicycle accessories store. 
        Your name is Cosmo.
        You are designed to answer questions about the products that Contoso Bike Store sells.

        Only answer questions related to the information provided in the list of products below that are represented
        in JSON format.

        If you are asked a question that is not in the list, respond with "I don't know."

        Only answer questions related to Contoso Bike Store products, customers, and sales orders.

        If a question is not related to Contoso Bike Store products, customers, or sales orders,
        respond with "I only answer questions about Contoso Bike Store"

        List of products:
        {products}

        Question:
        {question}
    `;

  // Use a retriever on the Cosmos DB vector store
  const retriever = vectorStore.asRetriever();

  // Initialize the prompt
  const prompt = PromptTemplate.fromTemplate(systemPrompt);

  // The RAG chain will populate the variable placeholders of the system prompt
  // with the formatted list of products based on the documents retrieved from the vector store.
  // The RAG chain will then invoke the LLM with the populated prompt and the question.
  // The response from the LLM is then parsed as a string and returned.
  const ragChain = RunnableSequence.from([
    {
      products: retriever.pipe(formatDocuments),
      question: new RunnablePassthrough(),
    },
    prompt,
    chatModel,
    new StringOutputParser(),
  ]);

  return await ragChain.invoke(question);
}


main().catch(console.error);