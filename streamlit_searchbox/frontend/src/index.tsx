import React from "react";
import ReactDOM from "react-dom";
import Searchbox from "./Searchbox";

import { Provider as StyletronProvider } from "styletron-react";
import { Client as Styletron } from "styletron-engine-atomic";

const engine = new Styletron();

ReactDOM.render(
  <StyletronProvider value={engine}>
    <React.StrictMode>
      <Searchbox />
    </React.StrictMode>
  </StyletronProvider>,
  document.getElementById("root"),
);
