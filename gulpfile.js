/// <binding BeforeBuild='default' />
var gulp = require('gulp');
var gutil = require('gulp-util');
var bower = require('bower');
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var minifyCss = require('gulp-minify-css');
var rename = require('gulp-rename');
var sh = require('shelljs');
var replace = require('replace');

var paths = {
  sass: ['./scss/**/*.scss']
};

var replaceFiles = ['./www/js/app.js'];

gulp.task('default', ['sass']);

gulp.task('add-proxy', function () {
    return replace({
        regex: "http://localhost:4000/images",
        replacement: "http://localhost:8100/images",
        paths: replaceFiles,
        recursive: false,
        silent: false,
    });
})

gulp.task('remove-proxy', function () {
    return replace({
        regex: "http://localhost:8100/images",
        replacement: "http://localhost:4000/images",
        paths: replaceFiles,
        recursive: false,
        silent: false,
    });
})

gulp.task('sass', function(done) {
  gulp.src('./scss/ionic.app.scss')
    .pipe(sass())
    .on('error', sass.logError)
    .pipe(gulp.dest('./www/css/'))
    .pipe(minifyCss({
      keepSpecialComments: 0
    }))
    .pipe(rename({ extname: '.min.css' }))
    .pipe(gulp.dest('./www/css/'))
    .on('end', done);
});

gulp.task('watch', function () {
    gulp.watch(paths.sass, ['sass']);
});
