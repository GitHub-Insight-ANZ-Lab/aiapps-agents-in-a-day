// config-template.js
// Copy this file to config.js and replace the placeholder values with your actual Azure OpenAI credentials

module.exports = {
  endpoint: "https://<AZURE_OPENAI_API_INSTANCE_NAME>.openai.azure.com/",
  apiKey: "<AZURE_OPENAI_API_KEY>",
  deploymentName: "completions" // or your specific deployment name
};

// Example:
// module.exports = {
//   endpoint: "https://my-openai-instance.openai.azure.com/",
//   apiKey: "abc123def456...",
//   deploymentName: "gpt-35-turbo"
// };