import React, { useState, useEffect, useRef } from "react";
import { trackPromise } from "react-promise-tracker";
import { usePromiseTracker } from "react-promise-tracker";
import * as sdk from 'microsoft-cognitiveservices-speech-sdk';

const Page = () => {
    const { promiseInProgress } = usePromiseTracker();
    const [speechText, setSpeechText] = useState<string>("");
    const synthesizerRef = useRef<sdk.SpeechSynthesizer | null>(null);
    const speechConfigRef = useRef<sdk.SpeechConfig | null>(null);

    useEffect(() => {
        const speech_key = '<YOUR_AZURE_SPEECH_KEY_HERE>';
        const speech_region = 'eastus';
        
        speechConfigRef.current = sdk.SpeechConfig.fromSubscription(
            speech_key,
            speech_region
        );
        
        speechConfigRef.current.speechSynthesisVoiceName = 'en-US-AriaNeural';
        speechConfigRef.current.speechSynthesisOutputFormat = 
            sdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3;
        
        synthesizerRef.current = new sdk.SpeechSynthesizer(
            speechConfigRef.current
        );

        return () => {
            if (synthesizerRef.current) {
                synthesizerRef.current.close();
            }
        };
    }, []);

    async function process() {
        if (speechText && synthesizerRef.current) {
            trackPromise(speechApi(speechText));
        }
    }

    async function speechApi(text: string): Promise<void> {
        return new Promise((resolve, reject) => {
            if (!synthesizerRef.current) {
                reject(new Error('Speech synthesizer not initialized'));
                return;
            }

            synthesizerRef.current.speakTextAsync(
                text,
                result => {
                    if (result.reason === sdk.ResultReason.SynthesizingAudioCompleted) {
                        console.log('Speech synthesis completed');
                        // Audio is automatically played by the SDK
                        resolve();
                    } else {
                        reject(new Error('Speech synthesis failed'));
                    }
                },
                error => {
                    console.error('Speech synthesis error:', error);
                    reject(error);
                }
            );
        });
    }

    const updateText = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSpeechText(e.target.value);
    };

    return (
        <div className="pageContainer">
            <h2>Speech</h2>
            <p>Enter text below to hear it spoken aloud using Azure Speech Services.</p>
            <div>
                <input 
                    type="text" 
                    placeholder="(enter some text to be read aloud)" 
                    value={speechText}
                    onChange={updateText}
                    style={{ width: '300px', marginRight: '10px' }}
                />
                <button onClick={process} disabled={!speechText || promiseInProgress}>
                    Read
                </button>
                <br />
                {promiseInProgress && <span>Processing speech...</span>}
            </div>
        </div>
    );
};

export default Page;