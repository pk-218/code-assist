import * as vscode from 'vscode';
import axios from 'axios';
import { getSelectionRange } from '../utils';

const getWebViewContent = (res: string) => {
    return `<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Optimise Code</title>
            <link
                rel="stylesheet"
                href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/a11y-dark.min.css"
                integrity="sha512-Vj6gPCk8EZlqnoveEyuGyYaWZ1+jyjMPg8g4shwyyNlRQl6d3L9At02ZHQr5K6s5duZl/+YKMnM3/8pDhoUphg=="
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
            />
            <script
                src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"
                integrity="sha512-bgHRAiTjGrzHzLyKOnpFvaEpGzJet3z4tZnXGjpsCcqOnAH6VGUx9frc5bcIhKTVLEiCO6vEhNAgx5jtLUYrfA=="
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
            ></script>
            <script>
                hljs.highlightAll();
            </script>
        </head>
        <body>
            <h1>Code Optimisation results</h1>
            <p>The following optimisations are suggested</p>
            <pre><code class="language-python">
${res}
            </code></pre>
            <button onClick="acceptChange()" id="accept-button">Accept</button>
            <button onClick="rejectChange()" id="reject-button">Reject</button>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.5.0/prism.min.js"></script>
        </body>
        <script>
            function acceptChange() {
                const vscode = acquireVsCodeApi();
                vscode.postMessage({
                    command: 'accept',
                });
            }
    
            function rejectChange() {
                const vscode = acquireVsCodeApi();
                vscode.postMessage({
                    command: 'reject',
                });
            }
        </script>
    
        <style>
            * {
                font-size: 16px;
            }
    
            button {
                font-size: 16px;
                border: none;
                padding: 5px;
            }
    
            #accept-button {
                background-color: greenyellow;
            }
    
            #reject-button {
                background-color: red;
                color: white;
            }
        </style>
    </html>
    
    `;
};

const optimiseCode = async (context: vscode.ExtensionContext) => {
    const editor = vscode.window.activeTextEditor;
    const selection = editor?.selection;

    if (selection && !selection.isEmpty) {
        const selectionRange = getSelectionRange(selection);
        const highlightedCode = editor.document.getText(selectionRange);

        console.log(highlightedCode);

        const panel = vscode.window.createWebviewPanel(
            'optimiseCode',
            'Optimise Code',
            vscode.ViewColumn.Beside,
            { enableScripts: true }
        );

        const {
            data: { ans },
        } = await axios.post('http://localhost:8000/optimize-code', {
            language: 'python',
            code: highlightedCode,
        });

        const res = ans.choices[0].message.content;

        console.log(res);
        panel.webview.html = getWebViewContent(res);

        panel.webview.onDidReceiveMessage((message) => {
            switch (message.command) {
                case 'accept':
                    editor.edit((editBuilder) => {
                        editBuilder.replace(
                            selectionRange,
                            ans.choices[0].message.content
                        );
                    });
                    return;
                case 'reject':
                default:
                    return;
            }
        });
    }
};


export default optimiseCode;