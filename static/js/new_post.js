var remns = {};
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
        console.log(remns.post_id);
        postService[action](post, remns.post_id);
    });

    var opts = {
      clientSideStorage: false,
      basePath: '/static/admin/epiceditor',
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
    };

    var editor = new EpicEditor(opts).load();
    return editor;
};
$(function() {

    var existingTags = [{id:1, name:'java'}, {id:2, name: 'Python'}, {id:3, name: 'Ruby'}];
    console.log(existingTags);

    var remns = remns || {};
    // postTags is an array of objects, {value: '', status: 'created/existing'}
    remns.postTags = [];
    window.tags = remns.postTags;
    $('#add-tags').selectize(
        {
            options: existingTags,
            labelField: 'name',
            searchField: 'name',
            valueField: 'id',
            highlight: false,
            create: true,
            closeAfterSelect: true,
            onItemAdd: function(d) {
                console.log('item added!');
                console.log(d);
                for(var i=0; i < existingTags.length; i+=1) {
                    var option = existingTags[i];
                    if(option.id === parseInt(d)) {
                        console.log('exisiting item!');
                        remns.postTags.push({
                            "value": option.id,
                            "status": 'existing'

                        });
                        return;
                    }
               } 
               console.log('created item!');
               remns.postTags.push({
                "value": d,
                "status": "created"
               });
        },
        onItemRemove: function(d) {
            console.log('item removed!');
            console.log(d);
            for(var i=0; i< remns.postTags.length; i+=1) {
                var addedTag = remns.postTags[i];
                if(addedTag.value === d || addedTag.value === parseInt(d)) {
                    console.log('exists!');
                    var temp = remns.postTags.splice(i);
                    remns.postTags = remns.postTags.concat(temp.splice(1, temp.length));
                    return;
                }
            }
        }
   });
});
   
