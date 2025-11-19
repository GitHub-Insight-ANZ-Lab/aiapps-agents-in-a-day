import React, { useState } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import { OpenAIClient, AzureKeyCredential, Completions } from '@azure/openai';

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [imageText, setImageText] = useState<string>();
    const [imageUrl, setImageUrl] = useState<string>("");

    async function process() {
        if (imageText != null) {
            trackPromise(
                dalleApi(imageText)
            ).then((res) => {
                setImageUrl(res);
            })
        }
    }

    async function dalleApi(prompt: string): Promise<string> {
        const size = '1024x1024';
        const n = 1;
        
        var openai_url = "https://aiaaa-s2-openai.openai.azure.com/";
        var openai_key = "<YOUR_AZURE_OPENAI_KEY_HERE>";
        const client = new OpenAIClient(
            openai_url,
            new AzureKeyCredential(openai_key),
            { apiVersion: "2024-02-01" }
        );

        const deploymentName = 'dalle3';
        const result = await client.getImages(deploymentName, prompt, { n, size });
        console.log(result);

        if (result.data[0].url) {
            return result.data[0].url;
        } else {
            throw new Error("Image URL is undefined");
        }
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setImageText(e.target.value);
    };

    return (
        <div className="pageContainer">
            <h2>Design</h2>
            <p></p>
            <p>
                <input type="text" placeholder="(describe your design here)" onChange={updateText} />
                <button onClick={() => process()}>Generate</button><br />
                {
                    (promiseInProgress === true) ?
                        <span>Loading...</span>
                        :
                        null
                }
            </p>
            <p>
                <img height={"550px"} src={imageUrl} />
            </p>
        </div>
    );
};

export default Page;