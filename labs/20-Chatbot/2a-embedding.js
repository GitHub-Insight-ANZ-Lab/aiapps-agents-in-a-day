require('dotenv').config();
const { MongoClient } = require('mongodb');

// set up the MongoDB client
const dbClient = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
var dbname = process.env.MONGODB_Name;

async function main() {
    try {
        await dbClient.connect();
        console.log('Connected to MongoDB');
        const db = dbClient.db(dbname); 
        console.log(await generateEmbeddings("Hello, world!"));

        
    } catch (err) {
        console.error(err);
    } finally {
        await dbClient.close();
        console.log('Disconnected from MongoDB');
    }
}

async function generateEmbeddings(text) {
  const embeddings = await aoaiClient.getEmbeddings(
    embeddingsDeploymentName,
    text
  );
  // Rest period to avoid rate limiting on Azure OpenAI
  await new Promise((resolve) => setTimeout(resolve, 500));
  return embeddings.data[0].embedding;
}

main().catch(console.error);

const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

// set up the Azure OpenAI client
const embeddingsDeploymentName = "embeddings";
const completionsDeploymentName = "gpt-4o";
const aoaiClient = new OpenAIClient(
  "https://" +
    process.env.AZURE_OPENAI_API_INSTANCE_NAME +
    ".openai.azure.com/",
  new AzureKeyCredential(process.env.AZURE_OPENAI_API_KEY)
);