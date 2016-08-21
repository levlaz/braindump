var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var cleanCSS = require('gulp-clean-css');
var sass = require('gulp-sass');

var vendor = {
  css: [
    'node_modules/bootstrap/dist/css/bootstrap.min.css',
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

  gulp.src('node_modules/bootstrap/dist/fonts/*')
        .pipe(gulp.dest(dist.fonts))
  ;
});

gulp.task('sass', function () {
  return gulp.src('./frontend/sass/**/*.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(concat('app.min.css'))
    .pipe(cleanCSS())
    .pipe(gulp.dest(dist.css));
});

gulp.task('sass:watch', function () {
  gulp.watch('./frontend/sass/*.scss', ['sass']);
});

gulp.task('default', ['vendor', 'sass:watch']);
