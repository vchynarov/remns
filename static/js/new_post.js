remns = {};
remns.post_id = null; // If there is an existing post.
remns.init = function() {
    var getParams = function(mode) {
        var post = {};
        post.title = $('[name=post-title]').val();
        post.content = editor.exportFile();
        post.mode = mode;
        return post;
    };

    var postService = new (function() {
       var request = function(method, post, id) {
           var url = '/admin/posts/';
           if(id) {
             url = '/admin/posts/' + id + '/';
           }
           $.ajax({
                type: method,
                url: url,
                data: post,
                success: function(data) {
                    window.location.replace("/admin/posts/");
                    if(data.status === 'success') {
                    }
                    else if(data.status === 'error') {
                    }
                }
            });
        };
        this.create = function(post, id) {
            request('POST', post, id);
        };
        this.update = function(post, id) {
            request('PUT', post, id);
        };
    })();



    $('.post-submit').click(function(evt) {
        var button = evt.target;
        var action = button.getAttribute('data-action');
        var mode = button.getAttribute('data-mode');
        var post = getParams(mode);
        console.log(remns.post_id)
        postService[action](post, remns.post_id);
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
   
