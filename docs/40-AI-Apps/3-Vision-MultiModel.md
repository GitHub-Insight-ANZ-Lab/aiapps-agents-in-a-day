---
title: "Computer Vision Analysis"
slug: /40-AI-Apps-Vision
---

:::info TUTORIAL OVERVIEW
In this tutorial, you'll learn how to leverage GPT-4o's advanced vision capabilities to analyze and extract valuable information from images in business applications.

**What you'll build:** An intelligent image analysis system that can understand, describe, and extract structured data from visual content using multi-modal AI.

**What you'll learn:**
- GPT-4o vision API integration and multi-modal prompt engineering
- Advanced image processing and base64 encoding techniques  
- Business-focused vision applications (quality control, inventory, document analysis)
- Production-ready error handling and content safety management
- Performance optimization for image processing workflows
- Integration patterns for vision-based automation systems

**Business Value:** Automate visual inspection processes, extract data from documents and images, enhance accessibility, and reduce manual processing time by 70-90%.
:::

## Understanding GPT-4o Vision Capabilities

### Revolutionary Multi-Modal AI

GPT-4o (Omni) represents a breakthrough in AI technology, combining advanced language understanding with sophisticated computer vision in a single model. This integration enables:

- **Unified Processing**: Seamless analysis of text and images together
- **Context Awareness**: Understanding relationships between visual and textual information
- **Advanced Reasoning**: Complex analysis combining visual observation with logical reasoning
- **Natural Language Output**: Descriptive, actionable insights in plain English

### Core Vision Capabilities

#### **Image Understanding**
- **Object Detection**: Identify and classify objects, people, animals, and products
- **Scene Analysis**: Understand environments, settings, and spatial relationships
- **Text Recognition**: Extract and interpret text within images (OCR capabilities)
- **Quality Assessment**: Evaluate image quality, defects, and compliance

#### **Document Analysis**
```typescript
interface DocumentAnalysis {
    documentType: 'invoice' | 'contract' | 'form' | 'receipt' | 'other';
    extractedText: string;
    keyFields: Record<string, string>;
    confidence: number;
    suggestedActions: string[];
}
```

#### **Technical Specifications**
- **Supported Formats**: JPEG, PNG, GIF, WebP
- **Resolution**: Up to 2048x2048 pixels (higher resolutions automatically resized)
- **File Size**: Up to 20MB per image
- **Processing Time**: Typically 2-10 seconds depending on complexity
- **Batch Processing**: Single image per request for optimal quality

### Business Applications by Industry

#### **Manufacturing & Quality Control**
```typescript
interface QualityInspection {
    productId: string;
    inspectionType: 'visual' | 'dimensional' | 'surface' | 'assembly';
    defectsDetected: DefectDetails[];
    qualityScore: number;
    passFailStatus: 'pass' | 'fail' | 'review';
    recommendations: string[];
}
```

**Use Cases:**
- Automated defect detection on production lines
- Component assembly verification
- Surface finish quality assessment
- Packaging inspection and compliance

#### **Healthcare & Medical**
- Medical imaging preliminary analysis
- Equipment monitoring and maintenance schedules
- Pharmaceutical packaging verification
- Accessibility compliance checking

#### **Retail & E-commerce**
- Product catalog image analysis and tagging
- Visual search implementation
- Inventory counting and management
- Brand compliance monitoring

#### **Financial Services**
- Document verification and KYC processes
- Insurance claim damage assessment
- Check processing and fraud detection
- Identity document validation

#### **Real Estate & Construction**
- Property condition assessments
- Construction progress monitoring
- Safety compliance verification
- Damage evaluation for insurance

## Learning Objectives

By the end of this tutorial, you will be able to:

1. Integrate GPT-4o vision capabilities for image analysis
2. Handle image uploads and base64 encoding
3. Create multi-modal prompts combining text and images
4. Build practical vision-based business solutions

## Scenario

Your customer service team needs to process product images efficiently. The goal is to deliver a seamless and efficient customer service experience that enhances operational accuracy and accelerates processing times through automated image analysis.

## Challenge

Leverage GPT-4o's vision capabilities for accurate analysis and verification of product photos. This reduces processing time while ensuring consistency and reliability in decision-making, ultimately enhancing the customer experience.

![Vision Challenge](images/challenge-3.png)

## Step-by-Step Implementation

### Step 1: Understanding GPT-4o Vision

GPT-4o with vision can:
- Analyze and describe images in detail
- Answer questions about visual content
- Identify objects, people, text in images
- Perform comparative analysis between images
- Extract structured data from visual information

### Step 2: Examine the Vision Component

Navigate to `apps-chat\chatbot\pages\vision\Vision.tsx`. You'll find:
- An image upload input for local files
- A text input for questions about the image
- A describe button to trigger analysis
- Display areas for the uploaded image and AI response

### Step 3: Implement Image Processing

Before sending to the vision API, you need to:
- Handle file uploads
- Convert images to base64 format
- Validate image types and sizes
- Prepare multi-modal messages

#### Key Functions to Implement:

```typescript
function getBase64(event) {
    // TODO: Convert uploaded file to base64
    // 1. Get the selected file from the event
    // 2. Create a FileReader instance
    // 3. Read the file as data URL (base64)
    // 4. Handle success and error cases
}
```

### Step 4: Implement the Vision API

Your task is to complete the `visionApi` function to:
- Construct multi-modal messages with text and image
- Send requests to GPT-4o vision endpoint
- Handle the API response
- Extract and return the analysis results

#### Message Structure:
```typescript
const messages = [
    { "role": "system", "content": "You are a helpful assistant." },
    {
        "role": "user", 
        "content": [
            {
                "type": "text",
                "text": userQuestion
            },
            {
                "type": "image_url",
                "imageUrl": {
                    "url": base64ImageData
                }
            }
        ]
    }
];
```

### Step 5: Advanced Vision Applications

#### Product Quality Inspection
```typescript
const systemPrompt = `You are a quality control inspector. 
Analyze the product image for:
- Manufacturing defects
- Damage or wear
- Compliance with specifications
- Overall condition assessment`;
```

#### Document Analysis
```typescript
const systemPrompt = `Extract and structure information from this document:
- Key data points
- Tables and forms
- Signatures and stamps
- Text content`;
```

#### Inventory Management
```typescript
const systemPrompt = `Analyze this inventory image:
- Count visible items
- Identify product types
- Assess organization and storage
- Note any issues or discrepancies`;
```

### Step 6: Error Handling and Validation

Implement robust error handling for:
- Unsupported file formats
- File size limitations
- Network connectivity issues
- API rate limiting
- Content policy violations

```typescript
async function validateImage(file: File): Promise<boolean> {
    // Check file type
    const supportedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!supportedTypes.includes(file.type)) {
        throw new Error('Unsupported file type');
    }
    
    // Check file size (example: 10MB limit)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        throw new Error('File too large');
    }
    
    return true;
}
```

## Solution Reference

<details>
<summary>View Complete Solution</summary>
<details>
<summary>Try implementing it yourself first!</summary>
<details>
<summary>Click to reveal the solution code</summary>

```typescript
import React, { useState } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import { OpenAIClient, AzureKeyCredential, Completions } from '@azure/openai';

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const [imageBase64, setImageBase64] = useState<string>("");
    const [imageText, setImageText] = useState<string>();
    const [imageDesc, setImageDesc] = useState<string>("");

    async function process() {
        if (imageText != null) {
            trackPromise(
                visionApi(imageText, imageBase64)
            ).then((res) => {
                setImageDesc(res);
            })
        }
    }

    async function visionApi(text: string, image: string): Promise<string> {
        const messages = [
            { "role": "system", "content": "You are a helpful assistant." },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "imageUrl": {
                            "url": `${image}`
                        }
                    }
                ]
            }
        ];

        const options = {
            api_version: "2024-08-01-preview"
        };

        const openai_url = "https://arg-syd-aiaaa-openai.openai.azure.com";
        const openai_key = "<API_KEY>";
        const client = new OpenAIClient(
            openai_url,
            new AzureKeyCredential(openai_key),
            options
        );

        const deploymentName = 'gpt4o';
        const result = await client.getChatCompletions(deploymentName, messages, {
            maxTokens: 200,
            temperature: 0.25
        });
        
        return result.choices[0]?.message?.content ?? '';
    }

    function getBase64(event: Event) {
        const file = (event.target as HTMLInputElement).files?.[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function () {
            setImageBase64(reader.result as string);
        };
        reader.onerror = function (error) {
            console.log('Error: ', error);
        };
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setImageText(e.target.value);
    };

    return (
        <div className="pageContainer">
            <h2>Vision</h2>

            <div>
                <input
                    type="file"
                    name="myImage"
                    accept="image/*"
                    onChange={(event) => {
                        setSelectedImage(event.target.files?.[0] || null);
                        getBase64(event);
                    }}
                />
                <br />

                {selectedImage && (
                    <div>
                        <h4>Your Photo</h4>
                        <p>
                            <img
                                width={"400px"}
                                src={URL.createObjectURL(selectedImage)}
                                alt="Uploaded image"
                            />
                        </p>

                        <h4>Question</h4>
                        <input 
                            type="text" 
                            placeholder="(your question about the image)" 
                            onChange={updateText} 
                        />
                        <p>
                            <button onClick={() => process()}>Describe</button><br />
                            {promiseInProgress && <span>Loading...</span>}
                        </p>
                        <p>{imageDesc}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Page;
```

</details>
</details>
</details>

## Real-World Applications

### Quality Control
- Automated defect detection in manufacturing
- Product compliance verification
- Damage assessment for insurance claims

### Retail and E-commerce
- Product categorization and tagging
- Visual search implementations
- Inventory management automation

### Healthcare
- Medical image preliminary analysis
- Equipment monitoring and maintenance
- Document processing and digitization

### Security and Surveillance
- Incident detection and reporting
- Access control verification
- Safety compliance monitoring

## Best Practices

### Performance Optimization
- Compress images before processing
- Implement caching for repeated analyses
- Use appropriate image resolutions
- Batch process multiple images when possible

### Security Considerations
- Validate all uploaded files
- Implement virus scanning
- Secure image storage and transmission
- Audit and log all processing activities

### User Experience
- Provide clear upload guidelines
- Show processing progress indicators
- Enable preview before processing
- Implement drag-and-drop functionality

## Integration Opportunities

Consider combining vision analysis with:

1. **Workflow Automation**: Trigger actions based on image content
2. **Database Integration**: Store analysis results for reporting
3. **Notification Systems**: Alert users to specific visual conditions
4. **ML Model Training**: Use results to improve custom models

## Next Steps

1. Move on to Tutorial 4: Speech Processing
2. Explore combining vision with other AI modalities
3. Build custom vision models for specific use cases
4. Implement real-time video analysis

## Additional Resources

- [GPT-4o Vision Documentation](https://docs.microsoft.com/azure/cognitive-services/openai/gpt-4-vision)
- [Computer Vision Best Practices](https://docs.microsoft.com/azure/cognitive-services/computer-vision/overview)
- [Image Processing Guidelines](https://docs.microsoft.com/azure/cognitive-services/openai/concepts/gpt-with-vision)
