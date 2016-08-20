var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var cleanCSS = require('gulp-clean-css');
var sass = require('gulp-sass');

var src = {
  css: [
    'frontend/css/style.css',
    'frontend/css/app.css',
    'frontend/css/notebook-card.css'
  ]
};

var vendor = {
  css: [
    'node_modules/bootstrap-tagsinput/src/bootstrap-tagsinput.css',
    'node_modules/font-awesome/css/font-awesome.min.css'
  ]
};

var dist = {
  fonts: 'app/static/fonts/',
  css: 'app/static/css/',
  img: 'app/static/img/'
};

gulp.task('vendor', function() {
  gulp.src(vendor.css)
    .pipe(concat('vendor.min.css'))
    .pipe(gulp.dest(dist.css))
  ;

  gulp.src('node_modules/font-awesome/fonts/*')
    .pipe(gulp.dest(dist.fonts))
  ;
});

gulp.task('css', function() {
  gulp.src(src.css)
    .pipe(concat('app.min.css'))
    .pipe(cleanCSS())
    .pipe(gulp.dest(dist.css))
  ;
});

gulp.task('sass', function () {
  return gulp.src('./frontend/sass/**/*.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(concat('app.min.css'))
    .pipe(cleanCSS())
    .pipe(gulp.dest(dist.css));
});

gulp.task('default', ['vendor', 'sass']);
