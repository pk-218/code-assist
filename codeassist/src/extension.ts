// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { optimiseCode } from './functions';
import { setDocString } from './addDocString';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export async function activate(context: vscode.ExtensionContext) {
    let optimiseCodeDisposable = vscode.commands.registerCommand(
        'codeassist.optimiseCode',
        () => optimiseCode(context)
    );
    let generateDocsDisposable = vscode.commands.registerCommand(
        'codeassist.generateDocs',
        async()=>{ 
            await setDocString(context);
        }
    );
    context.subscriptions.push(generateDocsDisposable);
    context.subscriptions.push(optimiseCodeDisposable);
    
    
}

// This method is called when your extension is deactivated
export function deactivate() {}
