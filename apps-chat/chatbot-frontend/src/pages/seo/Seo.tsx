import React, { useState } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import { OpenAIClient, AzureKeyCredential } from '@azure/openai';

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [seoUrl, setSeoUrl] = useState<string>("");
    const [seoText, setSeoText] = useState<string>("");

    async function process() {
        if (seoUrl) {
            trackPromise(
                seoApi(seoUrl)
            ).then((res) => {
                setSeoText(res);
            }).catch((error) => {
                console.error('SEO analysis failed:', error);
                setSeoText('Error analyzing the webpage. Please check the URL and try again.');
            });
        }
    }

    async function seoApi(url: string): Promise<string> {
        try {
            // Fetch webpage content
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();
            
            // Clean and extract meaningful content
            const cleanContent = cleanHtmlContent(html);
            
            // Prepare AI prompt for SEO analysis
            const messages = [
                { 
                    "role": "system", 
                    "content": `You are an SEO expert. Analyze the provided HTML content and generate SEO-optimized metadata. 
                    Return a valid JSON object with the following structure:
                    {
                        "seoTitle": "compelling page title (50-60 characters)",
                        "seoDescription": "engaging meta description (150-160 characters)",
                        "seoKeywords": ["keyword1", "keyword2", "keyword3"],
                        "focusKeyword": "primary keyword",
                        "suggestions": ["improvement suggestion 1", "suggestion 2"]
                    }
                    
                    Ensure the output is valid JSON format only.`
                },
                {
                    "role": "user", 
                    "content": `Analyze this webpage content and generate SEO metadata:\n\n${cleanContent}`
                }
            ];
            
            const openai_url = "https://aiaaa-s2-openai.openai.azure.com/";
            const openai_key = "<YOUR_AZURE_OPENAI_KEY_HERE>";
            const client = new OpenAIClient(
                openai_url,
                new AzureKeyCredential(openai_key),
                { apiVersion: "2024-08-01-preview" }
            );

            const deploymentName = 'gpt-4o';
            const result = await client.getChatCompletions(deploymentName, messages, {
                maxTokens: 500,
                temperature: 0.3
            });

            return result.choices[0]?.message?.content ?? 'No SEO analysis generated';
        } catch (error) {
            console.error('Error in seoApi:', error);
            throw error;
        }
    }

    function cleanHtmlContent(html: string): string {
        // Create a temporary DOM element to parse HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Remove script and style elements
        const scripts = doc.querySelectorAll('script, style');
        scripts.forEach(el => el.remove());
        
        // Extract text from important elements
        const title = doc.querySelector('title')?.textContent || '';
        const headings = Array.from(doc.querySelectorAll('h1, h2, h3, h4, h5, h6'))
            .map(el => el.textContent).join(' ');
        const paragraphs = Array.from(doc.querySelectorAll('p'))
            .map(el => el.textContent).join(' ');
        const metaDescription = doc.querySelector('meta[name="description"]')?.getAttribute('content') || '';
        
        // Combine and clean content
        const content = `Title: ${title}\nHeadings: ${headings}\nContent: ${paragraphs}\nMeta Description: ${metaDescription}`;
        
        // Clean whitespace and return
        return content.replace(/\s+/g, ' ').trim();
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSeoUrl(e.target.value);
    };

    return (
        <div className="pageContainer">
            <h2>SEO Content Generator</h2>
            <p>
                Analyze web pages and generate SEO-optimized content automatically.
                <br />
                Sample product page: <code>https://symmetrical-trout-7pg4x6xpp94hx9gq-4000.app.github.dev/product.html</code>
            </p>
            <div>
                <input 
                    type="url" 
                    placeholder="Enter webpage URL" 
                    value={seoUrl}
                    onChange={updateText}
                    style={{ width: '400px', marginRight: '10px' }}
                />
                <button onClick={process} disabled={!seoUrl || promiseInProgress}>
                    Generate SEO Content
                </button>
                <br />
                {promiseInProgress && <span>Analyzing webpage...</span>}
            </div>
            <div style={{ marginTop: '20px' }}>
                {seoText && (
                    <div>
                        <h3>Generated SEO Content:</h3>
                        <pre style={{ 
                            background: '#f5f5f5', 
                            padding: '10px', 
                            borderRadius: '5px',
                            whiteSpace: 'pre-wrap',
                            fontSize: '14px'
                        }}>
                            {seoText}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Page;