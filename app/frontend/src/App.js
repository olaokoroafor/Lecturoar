import React from "react";
import "./App.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Search from "./Search";
import ViewVideo from "./ViewVideo";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path={`/course/:courseId/video/:videoId/watch`}>
            <ViewVideo />
          </Route>
          <Route path="/">
            <Search />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
