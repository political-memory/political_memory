var gulp = require('gulp');
var less = require('gulp-less');
var watch = require('gulp-watch');
var minifycss = require('gulp-minify-css');
var rename = require('gulp-rename');
var gzip = require('gulp-gzip');
var livereload = require('gulp-livereload');

var gzip_options = {
    threshold: '1kb',
    gzipOptions: {
        level: 9
    }
};

var less_src = ['static/less/base.less', 'static/less/libs.less'];

/* Compile Our Sass */
gulp.task('less', function() {
    return gulp.src(less_src)
        .pipe(less())
        .pipe(gulp.dest('static/stylesheets'))
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest('static/stylesheets'))
        // .pipe(gzip(gzip_options))
        // .pipe(gulp.dest('static/stylesheets'))
        .pipe(livereload());
});

/* Watch Files For Changes */
gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('static/less/*.less', ['less']);

    /* Trigger a live reload on any Django template changes */
    gulp.watch('**/templates/*').on('change', livereload.changed);

});

gulp.task('default', ['less', 'watch']);
