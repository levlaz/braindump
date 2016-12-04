import requests from 'superagent';
import {browserHistory} from 'react-router';

// Action Types
export const AUTH_USER = 'AUTH_USER';
export const AUTH_ERROR = 'AUTH_ERROR';
export const SIGN_OUT_USER = 'SIGN_OUT_USER';