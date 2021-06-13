import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import BedNumberPage from "./pages/bedNumberPage";
import FallRiskStatusPage from "./pages/fallRiskStatusPage"
import ReadyPage from "./pages/readyPage"

const AppRouter = () => {
  return (
    <Router>
      <Switch>
        <Route exact path = "/" component = {ReadyPage} />
        <Route exact path = "/bednumber" component = {BedNumberPage} />
        <Route exact path = "/fallriskstatus" component = {FallRiskStatusPage} />
      </Switch>
    </Router>
  )
}

export default AppRouter;