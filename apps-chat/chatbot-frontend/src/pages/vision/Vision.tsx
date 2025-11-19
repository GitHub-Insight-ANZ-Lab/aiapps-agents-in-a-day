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


        const openai_url = "https://aiaaa-s2-openai.openai.azure.com/";
        const openai_key = "<YOUR_AZURE_OPENAI_KEY_HERE>";
        const client = new OpenAIClient(
            openai_url,
            new AzureKeyCredential(openai_key),
            { apiVersion: "2024-08-01-preview" }
        );

        const deploymentName = 'gpt-4o';
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