var gulp = require('gulp'),
    concat = require('gulp-concat'),
    path = require('path'),
    uglify = require('gulp-uglify');


var build_tasks = [
  'build-epiceditor',
  'build-vendor-css',
  'build-vendor-js',
  'build-admin-js',
  'move-templates'
];

var DISTDIR = 'remns/dist';
var dist = {
    'static': path.join(DISTDIR, 'static', 'admin'),
    'templates': path.join(DISTDIR, 'templates', 'admin'),
    'epiceditor': path.join(DISTDIR, 'static', 'admin', 'epiceditor')
};

gulp.task('default', build_tasks);

gulp.task('watch', function() {
    gulp.watch(remnsPaths.js.concat(remnsPaths.templates), build_tasks);
});
 
var bowerPaths = {
    'css' : [
        'bower_components/semantic-ui/dist/semantic.min.css',
     ],
    'js' : [
        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/epiceditor/epiceditor/js/epiceditor.js',
        'bower_components/semantic-ui/dist/semantic.js'
     ]
};

var remnsPaths = {
    'js' : [
        'static/js/*.js',
    ],
    'templates' : [
        'static/templates/*.html'
    ]
};

gulp.task('move-templates', function() {
    return gulp.src(remnsPaths.templates)
        .pipe(gulp.dest(dist.templates));
});

gulp.task('build-admin-js', function() {
    return gulp.src(remnsPaths.js)
        .pipe(concat('utils.js'))
        .pipe(uglify())
        .on('error', function(e) {
            console.log('Invalid JS file format.');
        })
        .pipe(gulp.dest(dist.static));

});
//
// epiceditor requires 'explicity' styling by providing links to CSS files.
gulp.task('build-epiceditor', function() {
    return gulp.src('bower_components/epiceditor/epiceditor/themes/**/*.css')
        .pipe(gulp.dest(dist.epiceditor));
});

gulp.task('build-vendor-css', function() {
    return gulp.src(bowerPaths.css)
        .pipe(concat('admin.css'))
        .pipe(gulp.dest(dist.static));
});

gulp.task('build-vendor-js', function() {
    return gulp.src(bowerPaths.js)
        .pipe(concat('admin.js'))
        .pipe(gulp.dest(dist.static));
});
