import React from "react";
import * as ReactDOMClient from "react-dom/client";
import App from "./App";
var container = document.getElementById("root");
var root = ReactDOMClient.createRoot(container);
root.render(React.createElement(React.StrictMode, null,
    React.createElement(App, null)));
//# sourceMappingURL=index.js.map