remns = {};
remns.init = function() {
    var getParams = function(mode) {
        var post = {};
        post.title = $('[name=post-title]').val();
        post.content = editor.exportFile();
        post.mode = mode;
        return post;
    };

    var savePost = function(post) {
        $.ajax({
            type: "POST",
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
    }

    $('#epiceditor-publish').click(function(evt) {
        var post = getParams('published');
        savePost(post);
    });

    $('#epiceditor-draft').click(function(evt) {
        var post = getParams('draft');
        savePost(post);
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
   
