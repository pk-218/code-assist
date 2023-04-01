import * as vscode from 'vscode';
import axios from 'axios';


const baseURL = 'http://localhost:8000';

export const setDocString = async(editor:vscode.TextEditor, highlightedCode: String,selectedRange: vscode.Range)=>{
    try{
        const {data} = await axios.post(`${baseURL}/docs`,{code:highlightedCode,language:"Python"});
        
        editor.edit((editBuilder)=>{
            editBuilder.replace(selectedRange,data);
        });
    }catch(err){
        console.log(err);
    }
    
};