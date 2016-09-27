'use strict';

import $ from 'jquery';
import jQuery from 'jquery';
window.$ = $;
window.jQuery = jQuery;

require('bootstrap');
require('bootstrap-tagsinput');
require('bootstrap-tabcollapse')

const editor = require('./braindump.editor');
const notebooks = require('./braindump.notebooks')
const dates = require('./Dates');

editor.initEditor();
notebooks.init();
dates.initDates();

$('#noteTabs').tabCollapse();
