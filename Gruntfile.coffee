module.exports = (grunt)->

  # Project configuration.
  grunt.initConfig({

    # LESS stuff
    less: {
      development: {
        options: {
        }
        files: {
          "css/main.css": "css/main.less"
        }
      } # end less:development
      production: {
        options: {
          compress: true
          cleancss: true
          strictImports: true
        }
        files: {
          "css/main.min.css": "css/main.less"
        }
      } # end less:production
    }
    # end LESS

    # Watch stuff
    watch: {
      options: {
        atBegin: true
        livereload: true
      }
      "less": {
        files: ['css/*.less']
        tasks: ['less']
      }
      "jinja-template": {
        files: ['template.jinja', 'data/**/*.yml']
        tasks: ['exec:generate-page']
      }
    }
    # end watch

    # Exec stuff
    exec: {
      "generate-page": {
        cmd: "python gen.py <%= env %>"
      }
    }
    # end exec

    'env': 'development' # default ENV

  })


  # Load the plugins for our tasks.
  grunt.loadNpmTasks('grunt-contrib-less')
  grunt.loadNpmTasks('grunt-contrib-watch')
  grunt.loadNpmTasks('grunt-exec')

  # Custom tasks
  grunt.registerTask('compile-all-prod', ()->
    grunt.task.run(['less:production', 'exec:generate-page'])
    grunt.config('env', 'production')
  )

  grunt.registerTask('compile-all-dev', ()->
    grunt.task.run(['less:development', 'exec:generate-page'])
    grunt.config('env', 'development')
  )

  # Default task(s).
  grunt.registerTask('default', ['compile-all-prod'])