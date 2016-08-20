'use strict';

import $ from 'jquery';
import jQuery from 'jquery';
window.$ = $;
window.jQuery = jQuery;

require('bootstrap');
require('bootstrap-tagsinput');

const editor = require('./braindump.editor');
const notebooks = require('./braindump.notebooks')
const dates = require('./Dates');

editor.initEditor();
editor.setActive();
notebooks.init();
dates.initDates();
