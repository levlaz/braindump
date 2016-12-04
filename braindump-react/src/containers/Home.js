import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as Actions from '../actions';
import logo from '../styles/images/logo.svg';
import '../styles/css/Home.css';

class Home extends React.Component {
    render() {
        return (
            <div className="Home">
                <div className="Home-header">
                    <img src={logo} className="Home-logo" alt="logo" />
                    <h2> Welcome to Braindump</h2>
                </div>
                    <p className="Home-intro">
                        Braindump is a simple, powerful and open note taking platform
                        that helps you organize your life. So far X people have organized
                        their lives with Y notes.
                    </p>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {};
}

function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(Actions, dispatch)
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);