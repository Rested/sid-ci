import React from 'react';
import './App.css';
import Repos from "./components/Repos";
import {Header} from "semantic-ui-react";

const App: React.FC = () => {
  // @ts-ignore
    return (
    <div className="App">
        <Header as="h1" dividing={true}>Sid CI</Header>
        <Repos/>
    </div>
  );
}

export default App;
