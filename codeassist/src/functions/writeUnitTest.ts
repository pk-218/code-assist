import * as vscode from "vscode";
import { getSelectionRange } from "../utils";
import axios from "axios";

const writeUnitTest = async (
  context: vscode.ExtensionContext,
  test_module: string
) => {
  const editor = vscode.window.activeTextEditor;
  const selection = editor?.selection;

  if (selection && !selection.isEmpty) {
    const selectionRange = getSelectionRange(selection);
    const highlightedCode = editor.document.getText(selectionRange);

    console.log(highlightedCode);

    try {
      const { data } = await axios.post("http://localhost:8000/ut", {
        code: highlightedCode,
        language: editor.document.languageId,
        test_module: test_module,
      });

      editor.edit((editBuilder) => {
        editBuilder.replace(selectionRange, data);
      });
    } catch (err) {
      console.log(err);
    }
  }
};

export default writeUnitTest;
