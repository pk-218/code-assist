import * as vscode from 'vscode';
import axios from 'axios';

const getWebViewContent = (data: string) => {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Optimise Code</title>
    </head>
    <body>
        <h1>Code Optimisation results</h1>
        <p>The following optimisations are suggested</p>
        <pre>${data}</pre>
        <button onClick="acceptChange()">Accept</button>
    </body>
    <script>
        function acceptChange() {
            const vscode = acquireVsCodeApi();
            vscode.postMessage({
                command: 'accept'
            })
        }
    </script>
    </html>`;
};

const optimiseCode = async (context: vscode.ExtensionContext) => {
    const editor = vscode.window.activeTextEditor;
    const selection = editor?.selection;

    if (selection && !selection.isEmpty) {
        const selectionRange = new vscode.Range(
            selection.start.line,
            selection.start.character,
            selection.end.line,
            selection.end.character
        );
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

        panel.webview.html = getWebViewContent(ans.choices[0].message.content);

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
                default:
                    return;
            }
        });
    }
};

export default optimiseCode;
