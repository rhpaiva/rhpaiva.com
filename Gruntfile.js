/*global module:false*/
module.exports = function(grunt) {

  var randomRange = function(min, max) {
      return Math.ceil(Math.random() * (max - min + 1));
  };

  // Project configuration.
  grunt.initConfig({

    paths: {
      'jslib': 'src/js',
      'jsdist': 'public/js',
      'csslib': 'src/css',
      'cssdist': 'public/css'
    },

    // Metadata.
    pkg: grunt.file.readJSON('package.json'),

    banner: '/*! <%= pkg.title || pkg.name %> - v<%= pkg.version %> - ' +
            '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
            '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' +
            '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>;' +
            ' Licensed <%= _.pluck(pkg.licenses, "type").join(", ") %> */\n',

    // Task configuration.
    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: true
      },
      dist: {
        //src: ['<%= paths.jslib + "/" + pkg.name %>.js'],
        src: ['<%= paths.jslib %>/**/**.js'],
        dest: '<%= paths.jsdist + "/" + pkg.name + "-" + pkg.version %>.js'
      }
    },

    uglify: {
      options: {
        banner: '<%= banner %>'
      },
      dist: {
        src: '<%= concat.dist.dest %>',
        dest: '<%= paths.jsdist + "/" + pkg.name + "-" + pkg.version %>.min.js'
      }
    },

    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        unused: true,
        boss: true,
        eqnull: true,
        browser: true,
        globals: {
          jQuery: true
        }
      },
      gruntfile: {
        src: 'Gruntfile.js'
      },
      lib_test: {
        src: ['<%= paths.jslib %>/**/*.js', 'test/**/*.js']
      }
    },

    qunit: {
      files: ['test/**/*.html']
    },

    watch: {
      gruntfile: {
        files: '<%= jshint.gruntfile.src %>',
        tasks: ['jshint:gruntfile']
      },
      lib_test: {
        files: '<%= jshint.lib_test.src %>',
        tasks: ['jshint:lib_test', 'qunit']
      },
      assets: {
        files: [
          '<%= paths.csslib %>/**/*.less', 
          '<%= paths.jslib %>/**/*.js'
        ],
        tasks: ['less', 'string-replace', 'concat', 'uglify']
      },
    },

    less: {
      development: {
        files: {
          //'<%= paths.cssdist + "/" + pkg.name + "-" + pkg.version %>.css': '<%= paths.csslib %>/**/*.less',
          '<%= paths.cssdist + "/" + pkg.name + "-" + pkg.version %>.css': '<%= paths.csslib %>/main.less',
        }
      }
    },

    'string-replace': {
      dist: {
        files: {
          '<%= paths.cssdist %>/': '<%= paths.cssdist %>/**/*.css',
          'templates/': 'templates/**/*.html'
        },
        options: {
          replacements: [{
            // replaces the number of the banner bg in less files
            pattern: /\%banner_number\%/ig,
            replacement: randomRange(1,9)
          }, {
            pattern: /\%version\%/,
            replacement: '<%= pkg.version %>'
          }]
        }
      }
    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  //grunt.loadNpmTasks('grunt-contrib-qunit');
  //grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-string-replace');

  // Default task.
  //grunt.registerTask('default', ['jshint', 'qunit', 'concat', 'uglify']);
  grunt.registerTask('default', ['less', 'string-replace', 'concat', 'uglify']);

};
