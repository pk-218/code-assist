

import * as vscode from "vscode";
import { optimiseCode, writeUnitTest,setDocString } from "./functions";
import { CodeAssistPanel } from "./view/CodeAssistPanel";
export async function activate(context: vscode.ExtensionContext) {
  let optimiseCodeDisposable = vscode.commands.registerCommand(
    "codeassist.optimiseCode",
    () => optimiseCode(context)
  );
  let generateDocsDisposable = vscode.commands.registerCommand(
    "codeassist.generateDocs",
    async () => {
      await setDocString(context);
    }
  );

  context.subscriptions.push(generateDocsDisposable);
  context.subscriptions.push(optimiseCodeDisposable);
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "codeassist.writeUnitTestPytest",
      async () => {
        await writeUnitTest(context, "pytest");
      }
    )
  );
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "codeassist.writeUnitTestUnittest",
      async () => {
        await writeUnitTest(context, "unittest");
      }
    )
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("codeassist.webview", () => {
      CodeAssistPanel.render(context.extensionUri);
    })
  );
}

// This method is called when your extension is deactivated
export function deactivate() {}
