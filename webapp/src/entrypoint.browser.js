import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { createStore } from "redux";
import AppReducer from "./reducers";
import App from "./component/app";

const appInitialState = window.__INITIAL__STATE__;
const store = createStore(
  AppReducer,
  appInitialState,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

delete window.__INITIAL__STATE__;

ReactDOM.hydrate(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);