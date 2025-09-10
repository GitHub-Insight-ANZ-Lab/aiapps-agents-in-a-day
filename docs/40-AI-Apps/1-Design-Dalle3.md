---
title: "Design with DALL-E"
slug: /40-AI-Apps-Design
---

:::info TUTORIAL OVERVIEW
In this tutorial, you'll learn how to leverage AI for product design by integrating DALL-E image generation into a web application.

**What you'll build:** A design generation feature that creates visual concepts from text descriptions using Azure OpenAI's DALL-E 3 model.

**What you'll learn:**
- How to integrate DALL-E with Azure OpenAI Service
- Image generation API implementation and best practices
- Advanced prompt engineering for better results
- Error handling for content safety and API limitations
- UI integration patterns for AI-generated content
- Production considerations for image generation services

**Business Value:** Accelerate design workflows, reduce time-to-market for visual concepts, and enable non-designers to create professional visual content.
:::

## Understanding DALL-E and Image Generation AI

### What is DALL-E?

DALL-E 3 is OpenAI's most advanced image generation model, capable of creating highly detailed and accurate images from natural language descriptions. It's integrated into Azure OpenAI Service, providing enterprise-grade capabilities including:

- **High-Quality Generation**: Creates photorealistic and artistic images
- **Prompt Adherence**: Better understanding of complex descriptions
- **Style Versatility**: Supports various artistic styles and formats
- **Content Safety**: Built-in filtering to prevent inappropriate content
- **Commercial Licensing**: Suitable for business and commercial use

### Key Capabilities

#### **Artistic Styles**
- Photorealistic imagery
- Digital art and illustrations
- Vintage and retro styles
- Minimalist and modern designs
- Abstract and conceptual art

#### **Technical Specifications**
- **Resolution**: 1024x1024, 1792x1024, 1024x1792 pixels
- **Format**: PNG with transparency support
- **Generation Time**: Typically 10-30 seconds per image
- **Prompt Length**: Up to 4000 characters
- **Batch Processing**: Single image per request (for quality)

#### **Business Applications**
- **Marketing Materials**: Social media graphics, advertisements, banners
- **Product Design**: Concept visualization, mockups, prototypes
- **Content Creation**: Blog illustrations, presentation graphics
- **Brand Assets**: Logo concepts, brand imagery, visual identity

## Learning Objectives

By the end of this tutorial, you will be able to:

1. **Technical Implementation**
   - Integrate DALL-E model for image generation using Azure OpenAI SDK
   - Implement secure API key management and authentication
   - Handle content safety exceptions and API errors gracefully
   - Create responsive UI components for AI-generated content

2. **Advanced Prompt Engineering**
   - Craft effective prompts for different design needs
   - Use style modifiers and technical specifications
   - Implement prompt templates for consistent results
   - Optimize prompts for commercial and business use cases

3. **Production Readiness**
   - Implement proper error handling and user feedback
   - Add loading states and progress indicators
   - Handle rate limiting and cost optimization
   - Integrate caching and storage solutions

4. **Business Integration**
   - Design workflows for creative teams
   - Implement approval and review processes
   - Add metadata and organization features
   - Create analytics and usage tracking

## Business Scenario Deep Dive

### The Challenge

You're working for **Contoso Design Agency**, a creative services company that helps businesses create compelling visual content. The design team faces several challenges:

- **Time Constraints**: Clients expect quick turnaround on concept development
- **Resource Limitations**: Limited designer availability for initial concepts
- **Creative Block**: Designers need inspiration and starting points
- **Cost Pressure**: Need to deliver more concepts within budget constraints
- **Diverse Needs**: Clients from various industries require different styles

### The Solution

Implement an AI-powered design generation system that:

1. **Accelerates Concept Development**: Generate multiple design variations in minutes
2. **Enhances Creativity**: Provides designers with diverse starting points
3. **Reduces Costs**: Enables junior designers and non-designers to create concepts
4. **Improves Client Satisfaction**: Deliver more options faster
5. **Scales Operations**: Handle more projects without proportional staff increases

### Success Metrics

- **Speed**: Reduce concept development time from hours to minutes
- **Volume**: Increase concept generation capacity by 300%
- **Quality**: Maintain professional standards with AI assistance
- **Cost**: Reduce per-concept cost by 50%
- **Satisfaction**: Improve client approval rates for initial concepts

### Real-World Use Cases

#### **Marketing Campaign Development**
```
Scenario: Creating social media graphics for a sustainable fashion brand
Prompt: "Modern minimalist Instagram post for sustainable fashion brand, 
        clean typography, earth tones, eco-friendly messaging, 
        professional photography style"
```

#### **Product Packaging Design**
```
Scenario: Developing packaging concepts for artisanal coffee
Prompt: "Coffee packaging design, artisanal craft aesthetic, 
        warm browns and golds, hand-drawn illustrations, 
        premium quality feel, suitable for retail display"
```

#### **Corporate Branding**
```
Scenario: Logo concepts for a technology startup
Prompt: "Technology startup logo, modern geometric design, 
        blue and gray color scheme, innovation and trust themes, 
        scalable for digital and print use"
```

## Scenario

You're tasked with developing a feature that helps product designers generate creative concepts quickly. The goal is to develop visually compelling designs that align with brand values and enhance brand identity, ensuring they captivate customer interest and drive engagement.

## Challenge

Elevate product design creativity by harnessing the power of DALL-E model to generate unique, high-quality artwork. This will facilitate concept development, streamline the brainstorming process, and inspire innovative design solutions that push creative boundaries.

![Design Challenge](images/challenge-1.png)

## Step-by-Step Implementation

### Step 1: Azure OpenAI Service Setup

Before implementing the code, ensure your Azure OpenAI Service is properly configured:

#### **Prerequisites Checklist**
- [ ] Azure subscription with OpenAI access approved
- [ ] Azure OpenAI resource created in supported region
- [ ] DALL-E 3 model deployed in your resource
- [ ] API keys and endpoint URLs available
- [ ] Network access configured (if using private endpoints)

#### **Service Configuration**
1. **Navigate to Azure Portal** → Azure OpenAI Service
2. **Create Deployment**: 
   - Model: `dall-e-3`
   - Deployment Name: `dalle3` (recommended)
   - Version: Latest available
3. **Note Configuration**:
   - Endpoint URL: `https://your-resource.openai.azure.com`
   - API Key: Available in "Keys and Endpoint" section
   - API Version: `2024-02-01` or later

#### **Testing Your Setup**
Use the Azure OpenAI Studio to test your deployment:
```bash
# Example test prompt
"A professional business logo design, modern and clean"
```

### Step 2: Development Environment Setup

#### **Install Required Dependencies**
The chatbot application already includes the necessary packages:
```json
{
  "@azure/openai": "^1.0.0-beta.12",
  "react-promise-tracker": "^2.1.1"
}
```

#### **Environment Variables**
Create or update your `.env` file:
```env
VITE_AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
VITE_AZURE_OPENAI_API_KEY=your-api-key-here
VITE_AZURE_OPENAI_API_VERSION=2024-02-01
VITE_DALLE_DEPLOYMENT_NAME=dalle3
```

### Step 3: Examine the Existing Code Structure

Navigate to `apps-chat/chatbot/src/pages/design/Design.tsx`. The current structure includes:

#### **Component State Management**
```typescript
const [imageText, setImageText] = useState<string>();    // User input
const [imageUrl, setImageUrl] = useState<string>("");    // Generated image URL
const { promiseInProgress } = usePromiseTracker();       // Loading state
```

#### **User Interface Elements**
- Input textbox for design descriptions
- Generate button to trigger AI image generation
- Image display area with responsive sizing
- Loading indicator during generation

#### **Current Limitations**
- Empty `dalleApi` function (needs implementation)
- No error handling for API failures
- No input validation or sanitization
- Limited user feedback during processing

### Step 4: Implement the Core DALL-E API Function

Your primary task is to complete the `dalleApi` function. Here's the comprehensive implementation approach:

#### **Basic Implementation Structure**
```typescript
async function dalleApi(prompt: string): Promise<string> {
    // 1. Validate and sanitize input
    // 2. Set up OpenAI client with configuration
    // 3. Configure image generation parameters
    // 4. Call the getImages method with deployment name
    // 5. Extract and validate image URL from response
    // 6. Handle errors and edge cases
    // 7. Return the generated image URL
}
```

#### **Implementation Requirements**

**Input Validation**
```typescript
// Validate prompt length and content
if (!prompt || prompt.trim().length === 0) {
    throw new Error('Please provide a description for your design');
}
if (prompt.length > 4000) {
    throw new Error('Description too long. Please keep it under 4000 characters');
}
```

**Client Configuration**
```typescript
// Configure Azure OpenAI client
const endpoint = process.env.VITE_AZURE_OPENAI_ENDPOINT;
const apiKey = process.env.VITE_AZURE_OPENAI_API_KEY;
const apiVersion = process.env.VITE_AZURE_OPENAI_API_VERSION;

const client = new OpenAIClient(endpoint, new AzureKeyCredential(apiKey), {
    apiVersion: apiVersion
});
```

**Generation Parameters**
```typescript
// Configure image generation settings
const size = '1024x1024';          // Standard square format
const quality = 'standard';        // Options: 'standard' | 'hd'
const style = 'vivid';            // Options: 'natural' | 'vivid'
const n = 1;                      // Number of images to generate
```

**Error Handling Strategy**
```typescript
try {
    const result = await client.getImages(deploymentName, prompt, options);
    return result.data[0]?.url || '';
} catch (error) {
    if (error.code === 'content_policy_violation') {
        throw new Error('Content was filtered for safety. Please try a different description.');
    } else if (error.code === 'rate_limit_exceeded') {
        throw new Error('Too many requests. Please wait a moment and try again.');
    } else if (error.code === 'insufficient_quota') {
        throw new Error('API quota exceeded. Please check your usage limits.');
    }
    throw new Error(`Image generation failed: ${error.message}`);
}
```

### Step 5: Advanced Prompt Engineering

#### **Effective Prompt Structure**
```typescript
const enhancePrompt = (userInput: string): string => {
    // Add style and quality specifications
    const styleModifiers = "professional, high quality, detailed";
    const technicalSpecs = "good lighting, sharp focus, 4k resolution";
    
    return `${userInput}, ${styleModifiers}, ${technicalSpecs}`;
};
```

#### **Prompt Templates for Common Use Cases**
```typescript
const promptTemplates = {
    logo: (description: string) => 
        `Professional logo design: ${description}, clean, modern, scalable vector style, suitable for business use`,
    
    product: (description: string) => 
        `Product photography: ${description}, professional studio lighting, white background, commercial quality`,
    
    illustration: (description: string) => 
        `Digital illustration: ${description}, artistic, creative, suitable for marketing materials`,
    
    social: (description: string) => 
        `Social media graphic: ${description}, engaging, modern design, optimized for digital platforms`
};
```

### Step 6: Enhanced User Experience Features

#### **Input Enhancement**
```typescript
// Add input suggestions and auto-complete
const designSuggestions = [
    "Modern minimalist logo for tech startup",
    "Vintage-style poster design for coffee shop", 
    "Professional headshot placeholder illustration",
    "Abstract background pattern for presentation"
];
```

#### **Progress Feedback**
```typescript
// Enhanced loading states
const [generationStatus, setGenerationStatus] = useState<string>('');

const statusMessages = [
    "Analyzing your description...",
    "Generating design concepts...", 
    "Finalizing image details...",
    "Almost ready!"
];
```

#### **Result Enhancement**
```typescript
// Add metadata and actions for generated images
interface GeneratedImage {
    url: string;
    prompt: string;
    timestamp: Date;
    dimensions: string;
    style: string;
}
```

## Advanced Features and Production Considerations

### Enhanced Implementation Features

#### **1. Multi-Size Generation Support**
```typescript
interface ImageGenerationOptions {
    size: '1024x1024' | '1792x1024' | '1024x1792';
    quality: 'standard' | 'hd';
    style: 'natural' | 'vivid';
}

async function generateImageWithOptions(
    prompt: string, 
    options: ImageGenerationOptions
): Promise<string> {
    const client = new OpenAIClient(endpoint, new AzureKeyCredential(apiKey));
    
    const result = await client.getImages(deploymentName, prompt, {
        n: 1,
        size: options.size,
        quality: options.quality,
        style: options.style
    });
    
    return result.data[0]?.url || '';
}
```

#### **2. Batch Generation and Variations**
```typescript
async function generateImageVariations(
    basePrompt: string, 
    variationCount: number = 3
): Promise<string[]> {
    const variations = [
        `${basePrompt}, style 1: photorealistic`,
        `${basePrompt}, style 2: artistic illustration`, 
        `${basePrompt}, style 3: minimalist design`
    ];
    
    const promises = variations.map(prompt => dalleApi(prompt));
    return Promise.all(promises);
}
```

#### **3. Smart Prompt Enhancement**
```typescript
class PromptEnhancer {
    static enhanceForBusiness(prompt: string): string {
        const businessModifiers = [
            "professional quality",
            "suitable for commercial use",
            "high resolution",
            "clean design"
        ];
        return `${prompt}, ${businessModifiers.join(', ')}`;
    }
    
    static enhanceForStyle(prompt: string, style: string): string {
        const styleGuides = {
            'corporate': 'clean, professional, modern, business-appropriate',
            'creative': 'artistic, imaginative, colorful, expressive',
            'minimal': 'simple, clean lines, white space, elegant',
            'vintage': 'retro, classic, aged, nostalgic'
        };
        
        return `${prompt}, ${styleGuides[style] || 'professional'}`;
    }
    
    static addTechnicalSpecs(prompt: string): string {
        return `${prompt}, high quality, detailed, professional lighting, 4k resolution`;
    }
}
```

#### **4. Content Safety and Validation**
```typescript
class ContentValidator {
    static validatePrompt(prompt: string): ValidationResult {
        const issues: string[] = [];
        
        // Length validation
        if (prompt.length > 4000) {
            issues.push('Prompt too long (max 4000 characters)');
        }
        
        // Content policy checks
        const restrictedTerms = ['violence', 'inappropriate', 'illegal'];
        const hasRestrictedContent = restrictedTerms.some(term => 
            prompt.toLowerCase().includes(term)
        );
        
        if (hasRestrictedContent) {
            issues.push('Content may violate policy guidelines');
        }
        
        return {
            isValid: issues.length === 0,
            issues: issues
        };
    }
}
```

#### **5. Caching and Performance Optimization**
```typescript
class ImageCache {
    private static cache = new Map<string, CacheEntry>();
    
    static async getOrGenerate(prompt: string): Promise<string> {
        const cacheKey = this.generateCacheKey(prompt);
        const cached = this.cache.get(cacheKey);
        
        if (cached && !this.isExpired(cached)) {
            return cached.imageUrl;
        }
        
        const imageUrl = await dalleApi(prompt);
        this.cache.set(cacheKey, {
            imageUrl,
            timestamp: Date.now(),
            expiryTime: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
        });
        
        return imageUrl;
    }
    
    private static generateCacheKey(prompt: string): string {
        return btoa(prompt.toLowerCase().trim()).slice(0, 32);
    }
    
    private static isExpired(entry: CacheEntry): boolean {
        return Date.now() > entry.expiryTime;
    }
}
```

### Production Deployment Considerations

#### **1. Security Best Practices**
```typescript
// Environment-based configuration
const config = {
    endpoint: process.env.AZURE_OPENAI_ENDPOINT,
    apiKey: process.env.AZURE_OPENAI_API_KEY,
    deploymentName: process.env.DALLE_DEPLOYMENT_NAME,
    maxRetries: parseInt(process.env.MAX_RETRIES) || 3,
    timeout: parseInt(process.env.REQUEST_TIMEOUT) || 30000
};

// Input sanitization
const sanitizePrompt = (input: string): string => {
    return input
        .trim()
        .replace(/[<>]/g, '') // Remove potential HTML
        .substring(0, 4000);   // Limit length
};
```

#### **2. Cost Management and Monitoring**
```typescript
class UsageTracker {
    static async trackGeneration(prompt: string, success: boolean): Promise<void> {
        const usage = {
            timestamp: new Date(),
            promptLength: prompt.length,
            success: success,
            estimatedCost: this.calculateCost(prompt),
            userId: this.getCurrentUserId()
        };
        
        // Log to analytics service
        await this.logUsage(usage);
    }
    
    private static calculateCost(prompt: string): number {
        // DALL-E 3 pricing: ~$0.040 per image (1024x1024)
        return 0.040;
    }
}
```

#### **3. Error Recovery and Resilience**
```typescript
async function dalleApiWithRetry(
    prompt: string, 
    maxRetries: number = 3
): Promise<string> {
    let lastError: Error;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await dalleApi(prompt);
        } catch (error) {
            lastError = error;
            
            // Don't retry on content policy violations
            if (error.code === 'content_policy_violation') {
                throw error;
            }
            
            // Exponential backoff
            if (attempt < maxRetries) {
                const delay = Math.pow(2, attempt) * 1000;
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }
    
    throw new Error(`Failed after ${maxRetries} attempts: ${lastError.message}`);
}
```

#### **4. Analytics and Monitoring**
```typescript
interface GenerationMetrics {
    totalGenerations: number;
    successRate: number;
    averageResponseTime: number;
    popularPromptPatterns: string[];
    errorDistribution: Record<string, number>;
}

class AnalyticsCollector {
    static async recordGeneration(
        prompt: string, 
        responseTime: number, 
        success: boolean,
        error?: string
    ): Promise<void> {
        const metrics = {
            timestamp: Date.now(),
            prompt: this.anonymizePrompt(prompt),
            responseTime,
            success,
            error: error || null,
            userAgent: navigator.userAgent,
            sessionId: this.getSessionId()
        };
        
        // Send to analytics service
        await fetch('/api/analytics/image-generation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(metrics)
        });
    }
}
```

### Integration with Business Workflows

#### **1. Approval Workflow Integration**
```typescript
interface DesignApproval {
    imageUrl: string;
    prompt: string;
    status: 'pending' | 'approved' | 'rejected';
    feedback?: string;
    approver?: string;
}

class ApprovalWorkflow {
    static async submitForReview(
        imageUrl: string, 
        prompt: string
    ): Promise<string> {
        const approval: DesignApproval = {
            imageUrl,
            prompt,
            status: 'pending'
        };
        
        // Submit to approval system
        const response = await fetch('/api/approvals', {
            method: 'POST',
            body: JSON.stringify(approval)
        });
        
        return response.json().approvalId;
    }
}
```

#### **2. Asset Management Integration**
```typescript
class AssetManager {
    static async saveToLibrary(
        imageUrl: string, 
        metadata: ImageMetadata
    ): Promise<AssetId> {
        // Download and store image
        const imageBlob = await fetch(imageUrl).then(r => r.blob());
        
        // Upload to asset management system
        const formData = new FormData();
        formData.append('image', imageBlob);
        formData.append('metadata', JSON.stringify(metadata));
        
        const response = await fetch('/api/assets', {
            method: 'POST',
            body: formData
        });
        
        return response.json().assetId;
    }
}
```

## Solution Reference and Examples

<details>
<summary>📚 Complete Implementation Guide</summary>

### Basic Implementation
<details>
<summary>🔧 Essential Code (Click to expand)</summary>

```typescript
import React, { useState } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import { OpenAIClient, AzureKeyCredential } from '@azure/openai';

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [imageText, setImageText] = useState<string>("");
    const [imageUrl, setImageUrl] = useState<string>("");
    const [error, setError] = useState<string>("");

    async function process() {
        if (!imageText?.trim()) {
            setError("Please enter a description for your design");
            return;
        }

        setError("");
        trackPromise(
            dalleApi(imageText)
        ).then((res) => {
            setImageUrl(res);
        }).catch((err) => {
            setError(err.message);
        });
    }

    async function dalleApi(prompt: string): Promise<string> {
        // Input validation
        if (!prompt || prompt.trim().length === 0) {
            throw new Error('Please provide a description for your design');
        }
        
        if (prompt.length > 4000) {
            throw new Error('Description too long. Please keep it under 4000 characters');
        }

        // Configuration
        const options = {
            api_version: "2024-02-01"
        };
        const size = '1024x1024';
        const quality = 'standard';
        const style = 'vivid';
        const n = 1;
        
        // Client setup
        const openai_url = process.env.VITE_AZURE_OPENAI_ENDPOINT || "your-endpoint-here";
        const openai_key = process.env.VITE_AZURE_OPENAI_API_KEY || "your-api-key-here";
        
        const client = new OpenAIClient(
            openai_url,
            new AzureKeyCredential(openai_key),
            options
        );

        try {
            const deploymentName = 'dalle3';
            const result = await client.getImages(deploymentName, prompt, { 
                n, 
                size, 
                quality, 
                style 
            });
            
            if (result.data[0]?.url) {
                return result.data[0].url;
            } else {
                throw new Error("Image generation failed - no URL returned");
            }
        } catch (error: any) {
            // Handle specific error types
            if (error.code === 'content_policy_violation') {
                throw new Error('Content was filtered for safety. Please try a different description.');
            } else if (error.code === 'rate_limit_exceeded') {
                throw new Error('Too many requests. Please wait a moment and try again.');
            } else if (error.code === 'insufficient_quota') {
                throw new Error('API quota exceeded. Please check your usage limits.');
            } else {
                throw new Error(`Image generation failed: ${error.message}`);
            }
        }
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setImageText(e.target.value);
        if (error) setError(""); // Clear error when user types
    };

    return (
        <div className="pageContainer">
            <h2>AI Design Generation</h2>
            <p>Describe your design concept and let AI create it for you.</p>
            
            {/* Input Section */}
            <div style={{ marginBottom: '20px' }}>
                <input 
                    type="text" 
                    placeholder="(describe your design here - e.g., modern logo for tech startup)" 
                    value={imageText}
                    onChange={updateText}
                    style={{ 
                        width: '400px', 
                        padding: '10px',
                        marginRight: '10px',
                        border: error ? '2px solid red' : '1px solid #ccc'
                    }}
                />
                <button 
                    onClick={process}
                    disabled={promiseInProgress || !imageText?.trim()}
                    style={{ 
                        padding: '10px 20px',
                        backgroundColor: promiseInProgress ? '#ccc' : '#0066cc',
                        color: 'white',
                        border: 'none',
                        cursor: promiseInProgress ? 'not-allowed' : 'pointer'
                    }}
                >
                    {promiseInProgress ? 'Generating...' : 'Generate Design'}
                </button>
            </div>

            {/* Error Display */}
            {error && (
                <div style={{ 
                    color: 'red', 
                    marginBottom: '20px',
                    padding: '10px',
                    backgroundColor: '#ffe6e6',
                    border: '1px solid #ff9999',
                    borderRadius: '4px'
                }}>
                    {error}
                </div>
            )}

            {/* Loading Indicator */}
            {promiseInProgress && (
                <div style={{ marginBottom: '20px' }}>
                    <span>🎨 Generating your design...</span>
                    <div style={{ 
                        width: '100%', 
                        height: '4px', 
                        backgroundColor: '#e0e0e0',
                        marginTop: '10px'
                    }}>
                        <div style={{
                            width: '30%',
                            height: '100%',
                            backgroundColor: '#0066cc',
                            animation: 'loading 2s infinite'
                        }}></div>
                    </div>
                </div>
            )}

            {/* Image Display */}
            {imageUrl && (
                <div style={{ marginTop: '20px' }}>
                    <h3>Generated Design:</h3>
                    <img 
                        src={imageUrl} 
                        alt="Generated design"
                        style={{ 
                            maxWidth: '100%', 
                            height: 'auto',
                            maxHeight: '550px',
                            border: '1px solid #ddd',
                            borderRadius: '8px',
                            boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
                        }} 
                    />
                    <div style={{ marginTop: '10px' }}>
                        <button 
                            onClick={() => window.open(imageUrl, '_blank')}
                            style={{ 
                                padding: '8px 16px',
                                marginRight: '10px',
                                backgroundColor: '#28a745',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer'
                            }}
                        >
                            View Full Size
                        </button>
                        <button 
                            onClick={() => {
                                const link = document.createElement('a');
                                link.href = imageUrl;
                                link.download = 'generated-design.png';
                                link.click();
                            }}
                            style={{ 
                                padding: '8px 16px',
                                backgroundColor: '#6c757d',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer'
                            }}
                        >
                            Download
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Page;
```

</details>

### Advanced Implementation
<details>
<summary>🚀 Production-Ready Features (Click to expand)</summary>

```typescript
import React, { useState, useCallback, useMemo } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import { OpenAIClient, AzureKeyCredential } from '@azure/openai';

// Types and Interfaces
interface GenerationOptions {
    size: '1024x1024' | '1792x1024' | '1024x1792';
    quality: 'standard' | 'hd';
    style: 'natural' | 'vivid';
}

interface GeneratedImage {
    url: string;
    prompt: string;
    timestamp: Date;
    options: GenerationOptions;
}

interface PromptSuggestion {
    category: string;
    prompt: string;
    description: string;
}

const AdvancedDesignPage = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [imageText, setImageText] = useState<string>("");
    const [generatedImages, setGeneratedImages] = useState<GeneratedImage[]>([]);
    const [error, setError] = useState<string>("");
    const [options, setOptions] = useState<GenerationOptions>({
        size: '1024x1024',
        quality: 'standard',
        style: 'vivid'
    });

    // Prompt suggestions
    const promptSuggestions: PromptSuggestion[] = useMemo(() => [
        {
            category: "Logos",
            prompt: "Modern minimalist logo for tech startup, clean geometric design",
            description: "Perfect for technology companies"
        },
        {
            category: "Marketing",
            prompt: "Social media post for coffee shop, warm browns, cozy atmosphere",
            description: "Great for food and beverage businesses"
        },
        {
            category: "Products",
            prompt: "Product packaging design, eco-friendly, sustainable materials",
            description: "Ideal for sustainable brands"
        }
    ], []);

    // Enhanced API function with retry logic
    const dalleApiAdvanced = useCallback(async (
        prompt: string, 
        options: GenerationOptions,
        retryCount: number = 0
    ): Promise<string> => {
        const maxRetries = 3;
        
        try {
            // Input validation
            if (!prompt || prompt.trim().length === 0) {
                throw new Error('Please provide a description for your design');
            }
            
            if (prompt.length > 4000) {
                throw new Error('Description too long. Please keep it under 4000 characters');
            }

            // Enhanced prompt with quality modifiers
            const enhancedPrompt = `${prompt}, professional quality, high resolution, suitable for commercial use`;

            // Client configuration
            const client = new OpenAIClient(
                process.env.VITE_AZURE_OPENAI_ENDPOINT || "",
                new AzureKeyCredential(process.env.VITE_AZURE_OPENAI_API_KEY || ""),
                { api_version: "2024-02-01" }
            );

            const result = await client.getImages('dalle3', enhancedPrompt, {
                n: 1,
                size: options.size,
                quality: options.quality,
                style: options.style
            });

            if (result.data[0]?.url) {
                return result.data[0].url;
            } else {
                throw new Error("Image generation failed - no URL returned");
            }

        } catch (error: any) {
            // Retry logic for transient errors
            if (retryCount < maxRetries && error.code !== 'content_policy_violation') {
                const delay = Math.pow(2, retryCount) * 1000; // Exponential backoff
                await new Promise(resolve => setTimeout(resolve, delay));
                return dalleApiAdvanced(prompt, options, retryCount + 1);
            }

            // Handle specific error types
            if (error.code === 'content_policy_violation') {
                throw new Error('Content was filtered for safety. Please try a different description.');
            } else if (error.code === 'rate_limit_exceeded') {
                throw new Error('Too many requests. Please wait a moment and try again.');
            } else {
                throw new Error(`Image generation failed: ${error.message}`);
            }
        }
    }, []);

    // Generate image with advanced options
    const generateImage = useCallback(async () => {
        if (!imageText?.trim()) {
            setError("Please enter a description for your design");
            return;
        }

        setError("");
        
        try {
            const imageUrl = await trackPromise(
                dalleApiAdvanced(imageText, options)
            );
            
            const newImage: GeneratedImage = {
                url: imageUrl,
                prompt: imageText,
                timestamp: new Date(),
                options: { ...options }
            };
            
            setGeneratedImages(prev => [newImage, ...prev]);
        } catch (err: any) {
            setError(err.message);
        }
    }, [imageText, options, dalleApiAdvanced]);

    // Apply suggestion
    const applySuggestion = useCallback((suggestion: PromptSuggestion) => {
        setImageText(suggestion.prompt);
        setError("");
    }, []);

    return (
        <div className="pageContainer" style={{ maxWidth: '1200px', margin: '0 auto' }}>
            <h2>🎨 AI Design Studio</h2>
            <p>Create professional designs with advanced AI image generation.</p>

            {/* Generation Controls */}
            <div style={{ 
                display: 'grid', 
                gridTemplateColumns: '1fr auto', 
                gap: '20px',
                marginBottom: '30px',
                padding: '20px',
                backgroundColor: '#f8f9fa',
                borderRadius: '8px'
            }}>
                {/* Input Section */}
                <div>
                    <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                        Design Description:
                    </label>
                    <textarea
                        value={imageText}
                        onChange={(e) => {
                            setImageText(e.target.value);
                            if (error) setError("");
                        }}
                        placeholder="Describe your design in detail... (e.g., modern logo for tech startup, blue and white colors, clean geometric design)"
                        style={{
                            width: '100%',
                            height: '100px',
                            padding: '12px',
                            border: error ? '2px solid #dc3545' : '1px solid #ced4da',
                            borderRadius: '4px',
                            fontSize: '14px',
                            resize: 'vertical'
                        }}
                    />
                    <div style={{ 
                        fontSize: '12px', 
                        color: '#6c757d', 
                        marginTop: '4px' 
                    }}>
                        {imageText.length}/4000 characters
                    </div>
                </div>

                {/* Options Panel */}
                <div style={{ minWidth: '200px' }}>
                    <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
                        Options:
                    </label>
                    
                    <div style={{ marginBottom: '12px' }}>
                        <label style={{ fontSize: '12px', marginBottom: '4px', display: 'block' }}>
                            Size:
                        </label>
                        <select
                            value={options.size}
                            onChange={(e) => setOptions(prev => ({ 
                                ...prev, 
                                size: e.target.value as GenerationOptions['size']
                            }))}
                            style={{ width: '100%', padding: '6px' }}
                        >
                            <option value="1024x1024">Square (1024×1024)</option>
                            <option value="1792x1024">Landscape (1792×1024)</option>
                            <option value="1024x1792">Portrait (1024×1792)</option>
                        </select>
                    </div>

                    <div style={{ marginBottom: '12px' }}>
                        <label style={{ fontSize: '12px', marginBottom: '4px', display: 'block' }}>
                            Quality:
                        </label>
                        <select
                            value={options.quality}
                            onChange={(e) => setOptions(prev => ({ 
                                ...prev, 
                                quality: e.target.value as GenerationOptions['quality']
                            }))}
                            style={{ width: '100%', padding: '6px' }}
                        >
                            <option value="standard">Standard</option>
                            <option value="hd">HD (Higher Cost)</option>
                        </select>
                    </div>

                    <div style={{ marginBottom: '16px' }}>
                        <label style={{ fontSize: '12px', marginBottom: '4px', display: 'block' }}>
                            Style:
                        </label>
                        <select
                            value={options.style}
                            onChange={(e) => setOptions(prev => ({ 
                                ...prev, 
                                style: e.target.value as GenerationOptions['style']
                            }))}
                            style={{ width: '100%', padding: '6px' }}
                        >
                            <option value="vivid">Vivid (More Creative)</option>
                            <option value="natural">Natural (More Realistic)</option>
                        </select>
                    </div>

                    <button
                        onClick={generateImage}
                        disabled={promiseInProgress || !imageText?.trim()}
                        style={{
                            width: '100%',
                            padding: '12px',
                            backgroundColor: promiseInProgress ? '#6c757d' : '#007bff',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: promiseInProgress ? 'not-allowed' : 'pointer',
                            fontSize: '14px',
                            fontWeight: 'bold'
                        }}
                    >
                        {promiseInProgress ? '🎨 Generating...' : '✨ Generate Design'}
                    </button>
                </div>
            </div>

            {/* Prompt Suggestions */}
            <div style={{ marginBottom: '30px' }}>
                <h3>💡 Prompt Suggestions</h3>
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
                    gap: '15px' 
                }}>
                    {promptSuggestions.map((suggestion, index) => (
                        <div
                            key={index}
                            onClick={() => applySuggestion(suggestion)}
                            style={{
                                padding: '15px',
                                border: '1px solid #dee2e6',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                backgroundColor: '#ffffff',
                                transition: 'all 0.2s',
                                ':hover': { backgroundColor: '#f8f9fa' }
                            }}
                        >
                            <div style={{ fontWeight: 'bold', marginBottom: '8px' }}>
                                {suggestion.category}
                            </div>
                            <div style={{ fontSize: '14px', marginBottom: '8px' }}>
                                "{suggestion.prompt}"
                            </div>
                            <div style={{ fontSize: '12px', color: '#6c757d' }}>
                                {suggestion.description}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Error Display */}
            {error && (
                <div style={{
                    color: '#721c24',
                    backgroundColor: '#f8d7da',
                    border: '1px solid #f5c6cb',
                    borderRadius: '4px',
                    padding: '12px',
                    marginBottom: '20px'
                }}>
                    ❌ {error}
                </div>
            )}

            {/* Loading Indicator */}
            {promiseInProgress && (
                <div style={{
                    textAlign: 'center',
                    padding: '40px',
                    backgroundColor: '#e3f2fd',
                    borderRadius: '8px',
                    marginBottom: '20px'
                }}>
                    <div style={{ fontSize: '18px', marginBottom: '10px' }}>
                        🎨 Creating your design...
                    </div>
                    <div style={{ fontSize: '14px', color: '#666' }}>
                        This may take 10-30 seconds
                    </div>
                </div>
            )}

            {/* Generated Images Gallery */}
            {generatedImages.length > 0 && (
                <div>
                    <h3>🖼️ Generated Designs ({generatedImages.length})</h3>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                        gap: '20px'
                    }}>
                        {generatedImages.map((image, index) => (
                            <div
                                key={index}
                                style={{
                                    border: '1px solid #dee2e6',
                                    borderRadius: '8px',
                                    overflow: 'hidden',
                                    backgroundColor: '#ffffff',
                                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                                }}
                            >
                                <img
                                    src={image.url}
                                    alt={`Generated design ${index + 1}`}
                                    style={{
                                        width: '100%',
                                        height: '250px',
                                        objectFit: 'cover'
                                    }}
                                />
                                <div style={{ padding: '15px' }}>
                                    <div style={{ 
                                        fontSize: '14px', 
                                        marginBottom: '10px',
                                        color: '#495057'
                                    }}>
                                        "{image.prompt}"
                                    </div>
                                    <div style={{
                                        fontSize: '12px',
                                        color: '#6c757d',
                                        marginBottom: '10px'
                                    }}>
                                        {image.timestamp.toLocaleString()} • {image.options.size} • {image.options.quality}
                                    </div>
                                    <div style={{ 
                                        display: 'flex', 
                                        gap: '8px',
                                        flexWrap: 'wrap'
                                    }}>
                                        <button
                                            onClick={() => window.open(image.url, '_blank')}
                                            style={{
                                                padding: '6px 12px',
                                                fontSize: '12px',
                                                backgroundColor: '#28a745',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: '4px',
                                                cursor: 'pointer'
                                            }}
                                        >
                                            View Full
                                        </button>
                                        <button
                                            onClick={() => {
                                                const link = document.createElement('a');
                                                link.href = image.url;
                                                link.download = `design-${index + 1}.png`;
                                                link.click();
                                            }}
                                            style={{
                                                padding: '6px 12px',
                                                fontSize: '12px',
                                                backgroundColor: '#6c757d',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: '4px',
                                                cursor: 'pointer'
                                            }}
                                        >
                                            Download
                                        </button>
                                        <button
                                            onClick={() => setImageText(image.prompt)}
                                            style={{
                                                padding: '6px 12px',
                                                fontSize: '12px',
                                                backgroundColor: '#007bff',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: '4px',
                                                cursor: 'pointer'
                                            }}
                                        >
                                            Reuse Prompt
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdvancedDesignPage;
```

</details>

### Testing Prompts and Examples
<details>
<summary>🧪 Test Cases and Example Prompts (Click to expand)</summary>

#### **Logo Design Prompts**
```typescript
const logoPrompts = [
    "Modern minimalist logo for tech startup, geometric design, blue and white colors",
    "Vintage coffee shop logo, hand-drawn style, warm browns and cream colors",
    "Medical clinic logo, clean and professional, cross symbol, green and blue",
    "Fitness gym logo, bold and energetic, dumbbells, red and black colors"
];
```

#### **Marketing Material Prompts**
```typescript
const marketingPrompts = [
    "Social media post for organic restaurant, fresh vegetables, natural lighting",
    "Banner for summer sale, bright and cheerful, 50% off text, retail style",
    "Event poster for music festival, colorful and vibrant, crowd silhouettes",
    "Product advertisement for luxury watch, elegant and sophisticated"
];
```

#### **Testing Scenarios**
```typescript
// Test error handling
const errorTestCases = [
    "", // Empty prompt
    "a".repeat(5000), // Too long prompt
    "violence and inappropriate content", // Content policy violation
];

// Test different sizes and qualities
const configTestCases = [
    { size: "1024x1024", quality: "standard", style: "natural" },
    { size: "1792x1024", quality: "hd", style: "vivid" },
    { size: "1024x1792", quality: "standard", style: "vivid" }
];
```

</details>

</details>

## Next Steps and Advanced Features

### Immediate Next Steps
1. **Complete the basic implementation** using the essential code example
2. **Test with various prompts** to understand capabilities and limitations
3. **Add error handling** to improve user experience
4. **Implement loading states** for better feedback

### Advanced Enhancements
1. **Multi-Generation**: Generate multiple variations of the same prompt
2. **Style Templates**: Pre-defined style modifiers for different use cases
3. **Image History**: Save and manage previously generated images
4. **Integration**: Connect with design asset management systems

### Integration Opportunities
Consider combining this tutorial with:
1. **Tutorial 3 (Vision)**: Analyze generated images for quality assessment
2. **Tutorial 2 (Translation)**: Generate designs for multiple language markets
3. **Tutorial 6 (Automation)**: Automate design workflows based on business rules

### Production Considerations
1. **Cost Management**: Monitor API usage and implement budgets
2. **Content Moderation**: Add additional safety checks beyond Azure's filters
3. **Performance**: Implement caching and optimize for mobile devices
4. **Analytics**: Track generation patterns and user preferences

## Additional Resources

- [Azure OpenAI DALL-E Documentation](https://docs.microsoft.com/azure/cognitive-services/openai/dall-e-quickstart)
- [Content Safety Guidelines](https://docs.microsoft.com/azure/cognitive-services/content-safety/)
- [OpenAI Client SDK Documentation](https://docs.microsoft.com/javascript/api/@azure/openai/)
