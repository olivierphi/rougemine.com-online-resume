import React from "react";
import ReactDOM from "react-dom";
import AppReducer from "./reducers";
import { Provider } from "react-redux";
import BioContainer from "container/bio";
import { createStore } from "redux";

const store = createStore(AppReducer);

ReactDOM.render(
  <Provider store={store}>
    <BioContainer />
  </Provider>,
  document.getElementById("root")
);
