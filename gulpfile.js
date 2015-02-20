var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('default', ['build-vendor-css', 'build-vendor-js']);

var adminPaths = {
    'css' : [
        'bower_components/semantic-ui/dist/semantic.min.css'
     ],
    'js' : [
        'bower_components/semantic-ui/dist/semantic.min.js'
     ]
};

gulp.task('build-vendor-css', function() {
    return gulp.src(adminPaths.css)
        .pipe(concat('admin.css'))
        .pipe(gulp.dest('static'));
});

gulp.task('build-vendor-js', function() {
    return gulp.src(adminPaths.js)
        .pipe(concat('admin.js'))
        .pipe(gulp.dest('static'));
});
