// Include gulp
var gulp = require('gulp'),
    uglify = require('gulp-uglify'), 
    minifyCSS = require('gulp-minify-css'),
    less = require('gulp-less'),
    autoprefixer = require('gulp-autoprefixer');

gulp.task('style', function () {
    return gulp.src('less/*.less')
        .pipe(less())
        .pipe(autoprefixer())
        .pipe(minifyCSS())
        .pipe(gulp.dest('../pages/static/css'));
});

gulp.task('scripts', function() {  
    return gulp.src('js/*.js')
        .pipe(uglify())
        .pipe(gulp.dest('../pages/static/js'))
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('less/**/*.less', ['style']);
    gulp.watch('js/*.js', ['scripts']);
});

// Default Task
gulp.task('default', ['style', 'scripts', 'watch']);
gulp.task('build', ['style', 'scripts']);