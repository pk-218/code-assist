import * as vscode from 'vscode';

const getWebViewContent = () => {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Optimise Code</title>
    </head>
    <body>
        <h1>Optimise Code</h1>
    </body>
    </html>`;
};

const optimiseCode = (context: vscode.ExtensionContext) => {
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
            {}
        );

        panel.webview.html = getWebViewContent();
    }
};

export default optimiseCode;
