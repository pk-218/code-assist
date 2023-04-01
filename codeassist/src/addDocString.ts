import * as vscode from 'vscode';
import axios from 'axios';


const baseURL = 'http://localhost:8000';

export const setDocString = async (context: vscode.ExtensionContext) => {
    vscode.window.showInformationMessage('Hello World from CodeAssist!');
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
        try {
            const { data } = await axios.post(`${baseURL}/docs`, { code: highlightedCode, language: "Python" });
    
            editor.edit((editBuilder) => {
                editBuilder.replace(selectionRange, data);
            });
        } catch (err) {
            console.log(err);
        }
    }

    

};