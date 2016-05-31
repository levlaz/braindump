'use strict';

import $ from 'jquery';
import jQuery from 'jquery';
window.$ = $;
window.jQuery = jQuery;

require('bootstrap');
require('bootstrap-tagsinput');

const editor = require('./braindumpEditor');
const dates = require('./Dates');

editor.initEditor();
dates.initDates();