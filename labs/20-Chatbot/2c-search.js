require("dotenv").config();
const { MongoClient } = require("mongodb");
const { OpenAIClient, AzureKeyCredential } = require("@azure/openai");

// set up the MongoDB client
const dbClient = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
var dbname = process.env.MONGODB_Name;

// set up the Azure OpenAI client
const embeddingsDeploymentName = "embeddings";
const aoaiClient = new OpenAIClient(
  "https://" +
  process.env.AZURE_OPENAI_API_INSTANCE_NAME +
  ".openai.azure.com/",
  new AzureKeyCredential(process.env.AZURE_OPENAI_API_KEY)
);

async function main() {
  try {
    await dbClient.connect();
    console.log("Connected to MongoDB");
    const db = dbClient.db(dbname);
    //vector search for the top 3 most relevant products
    const searchResults = await vectorSearch(
      db,
      "products",
      "What products do you have that are yellow?"
    );
    searchResults.forEach(printProductSearchResult);


  } catch (err) {
    console.error(err);
  } finally {
    await dbClient.close();
    console.log("Disconnected from MongoDB");
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

async function vectorSearch(db, collectionName, query, numResults = 3) {
  const collection = db.collection(collectionName);
  // generate the embedding for incoming question
  const queryEmbedding = await generateEmbeddings(query);

  const pipeline = [
    {
      $search: {
        cosmosSearch: {
          vector: queryEmbedding,
          path: "contentVector",
          k: numResults,
        },
        returnStoredSource: true,
      },
    },
    {
      $project: {
        similarityScore: { $meta: "searchScore" },
        document: "$$ROOT",
      },
    },
  ];

  //perform vector search and return the results as an array
  const results = await collection.aggregate(pipeline).toArray();
  return results;
}

function printProductSearchResult(result) {
  // Print the search result document in a readable format
  console.log(`Similarity Score: ${result["similarityScore"]}`);
  console.log(`Name: ${result["document"]["name"]}`);
  console.log(`Category: ${result["document"]["categoryName"]}`);
  console.log(`SKU: ${result["document"]["sku"]}`);
  console.log(`_id: ${result["document"]["_id"]}\n`);
}

main().catch(console.error);
