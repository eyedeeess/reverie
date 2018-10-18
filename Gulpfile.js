const gulp = require('gulp');

const css = require('gulp-clean-css');
const mjml = require('gulp-mjml');
const sass = require('gulp-sass');

gulp.task('emails', function() {
  return gulp.src('./assets/src/mjml/*.mjml')
    .pipe(mjml())
    .pipe(gulp.dest('./templates/email/'))
});

gulp.task('css', function() {
  return gulp.src('./assets/src/css/*.css')
    .pipe(css())
    .pipe(gulp.dest('./assets/dist/css/'))
});

gulp.task('sass', function() {
  return gulp.src('./assets/src/sass/*.sass')
    .pipe(sass({
      includePaths: [
        'node_modules/bulma',
        'node_modules/bulma-timeline/dist/css',
      ]
    }).on('error', sass.logError))
    .pipe(gulp.dest('./assets/dist/css/'))
});

gulp.task('default', ['emails', 'css', 'sass']);
