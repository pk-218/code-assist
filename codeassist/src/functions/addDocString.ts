import * as vscode from 'vscode';
import axios from 'axios';
import { BASE_URI } from '../constants';

const setDocString = async (context: vscode.ExtensionContext) => {
    // vscode.window.showInformationMessage('Hello World from CodeAssist!');
    const editor = vscode.window.activeTextEditor;
    const selection = editor?.selection;

    if (selection && !selection.isEmpty) {
        const selectionRange = new vscode.Range(
            selection.start.line,
            selection.start.character,
            selection.end.line,
            selection.end.character
        );
        let codeLanguage = 'javascript';
        if (editor.document.fileName.split('.')[1] === 'py') {
            codeLanguage = 'python';
        }
        const highlightedCode = editor.document.getText(selectionRange);

        try {
            const { data } = await axios.post(`${BASE_URI}/docs`, {
                code: highlightedCode,
                language: codeLanguage,
            });
            console.log(data);
            if (highlightedCode === data.code_with_docs) {
                vscode.window.showInformationMessage(
                    'No function definition found!'
                );
                return;
            }
            if (data.more_than_one_def) {
                vscode.window.showWarningMessage(
                    'More than one definitions detected, all will be documented in one doc String'
                );
            }
            editor.edit((editBuilder) => {
                editBuilder.replace(selectionRange, data.code_with_docs);
            });
        } catch (err) {
            console.log(err);
        }
    }
};

export default setDocString;
