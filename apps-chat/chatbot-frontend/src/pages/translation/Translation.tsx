import React, { useState } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [originalText, setOriginalText] = useState<string>();
    const [translatedText, setTranslatedText] = useState<string>("");

    async function process() {
        if (originalText != null) {
            trackPromise(
                translationApi(originalText)
            ).then((res) => {
                setTranslatedText(res);
            })
        }
    }

    async function translationApi(text: string): Promise<string> {
        const translation_url = `https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=fr&from=en`;
        const translation_key = "<YOUR_AZURE_TRANSLATOR_KEY_HERE>";

        const body = [{
            "text": `${text}`
        }];

        const response = await fetch(translation_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Region": "eastus",
                "Ocp-Apim-Subscription-Key": translation_key,
            },
            body: JSON.stringify(body),
        });
        
        const data = await response.json();
        return data[0].translations[0].text;
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setOriginalText(e.target.value);
    };

    return (
        <div className="pageContainer">
            <h2>Translation</h2>
            <p></p>
            <p>
                <input type="text" placeholder="(enter text in English to translate to French)" onChange={updateText} />
                <button onClick={() => process()}>Translate</button><br />
                {
                    (promiseInProgress === true) ?
                        <span>Loading...</span>
                        :
                        null
                }
            </p>
            <p>
                {translatedText}
            </p>
        </div>
    );
};

export default Page;