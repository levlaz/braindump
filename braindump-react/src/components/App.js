import React from 'react';
import Header from '../containers/Header';
import '../styles/css/app.css';

export default class App extends React.Component {
    render() {
        return (
            <div>
                <Header />
                {this.props.children}
            </div>
        );
    }
}