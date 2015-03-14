remns = {};
remns.init = function() {
    var getParams = function(mode) {
        var post = {};
        post.title = $('[name=post-title]').val();
        post.content = editor.exportFile();
        post.mode = mode;
        return post;
    };

    var postService = new (function() {
       var request = function(method, post) {
           $.ajax({
                type: method,
                url: "/admin/posts",
                data: post,
                success: function(data) {
                    console.log(data);
                    if(data.status === 'success') {
                    }
                    else if(data.status === 'error') {
                    }
                }
            });
        };
        this.create = function(post) {
            request('POST', post);
        };
        this.update = function(post) {
            request('PUT', post);
        };
    })();

    $('.post-submit').click(function(evt) {
        console.log(evt);
        var button = evt.target;
        console.log(button.getAttribute('data-state'));
        console.log(button.getAttribute('data-mode'));
    });

    var opts = {
      clientSideStorage: false,
      basePath: '/static/epiceditor',
      textarea: 'initial-content',
      theme: {
        base: '/base/epiceditor.css',
        preview: '/preview/preview-dark.css',
        editor: '/editor/epic-dark.css'
      },
      autogrow: {
        minHeight: 500,
        maxHeight: 500
      }
    }

    var editor = new EpicEditor(opts).load();
    return editor
}
remns.editor = remns.init();
   
