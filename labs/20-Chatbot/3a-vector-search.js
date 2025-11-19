
require('dotenv').config();
const { MongoClient } = require('mongodb');
const {
    AzureCosmosDBVectorStore,
    AzureCosmosDBSimilarityType,
} = require("@langchain/community/vectorstores/azure_cosmosdb");
const { OpenAIEmbeddings } = require("@langchain/openai");

const dbClient = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
var dbname = process.env.MONGODB_Name;
const azureCosmosDBConfig = {
    client: dbClient,
    databaseName: dbname,
    collectionName: "products",
    indexName: "VectorSearchIndex",
    embeddingKey: "contentVector",
    textKey: "_id",
};
const vectorStore = new AzureCosmosDBVectorStore(
    new OpenAIEmbeddings(),
    azureCosmosDBConfig
);


async function main() {
    try {
        await dbClient.connect();
        console.log("Connected to MongoDB");
        const results = await vectorStore.similaritySearch(
            "What yellow products do you have?",
            AzureCosmosDBSimilarityType.CosineSimilarity,
            3
        );
        console.log(results);


    } catch (err) {
        console.error(err);
    } finally {
        await dbClient.close();
        console.log('Disconnected from MongoDB');
    }
}

main().catch(console.error);