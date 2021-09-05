import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Notes from './pages/Notes'

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Notes />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
