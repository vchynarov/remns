var gulp = require('gulp'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify');

var build_tasks = [
  'build-epiceditor',
  'build-vendor-css',
  'build-vendor-js',
  'build-admin-js'
];

gulp.task('default', build_tasks);
 
var adminPaths = {
    'css' : [
        'bower_components/semantic-ui/dist/semantic.min.css',
     ],
    'js' : [
        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/epiceditor/epiceditor/js/epiceditor.js',
        'bower_components/semantic-ui/dist/semantic.js'
     ]
};

gulp.task('build-admin-js', function() {
    return gulp.src('static/js/*.js')
        .pipe(concat('utils.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist'));

});
// epiceditor requires 'explicity' styling by providing links to CSS files.
gulp.task('build-epiceditor', function() {
    return gulp.src('bower_components/epiceditor/epiceditor/themes/**/*.css')
        .pipe(gulp.dest('dist/epiceditor'));
});

gulp.task('build-vendor-css', function() {
    return gulp.src(adminPaths.css)
        .pipe(concat('admin.css'))
        .pipe(gulp.dest('dist'));
});

gulp.task('build-vendor-js', function() {
    return gulp.src(adminPaths.js)
        .pipe(concat('admin.js'))
        .pipe(gulp.dest('dist'));
});
