var remns = {};
remns.post_id = null; // If there is an existing post.
remns.init = function() {
    var getParams = function(mode, tags) {
        var post = {};
        post.title = $('[name=post-title]').val();
        post.content = editor.exportFile();
        post.mode = mode;
        post.tags = tags;
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
                data: JSON.stringify(post),
                contentType: 'application/json',
                success: function(data) {
                    if(data.status === 'success') {
                        window.location.replace("/admin/posts/");
                    }
                    else if(data.status === 'error') {
                        console.error('Error');
                        console.log(data);
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
        var tags = remns.postTags;
        var button = evt.target;
        var action = button.getAttribute('data-action');
        var mode = button.getAttribute('data-mode');
        var post = getParams(mode, tags);
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


remns.tagsInit = function() {
    remns.existingTags = [];
    // postTags is an array of objects, {value: '', status: 'created/existing'}
    remns.postTags = [];
    var q_all_tags = $.ajax({type: "GET", url: "/tags" });
    var q_existing_tags = remns.post_id ? $.ajax({type: "GET", url: "/posts/" + remns.post_id + "/tags/"}) : $.Deferred().resolve();
    $.when(q_all_tags, q_existing_tags).done(function(all_tags_response, existing_tags_response) {
        all_tags = all_tags_response ? all_tags_response[0] : [];
        existing_tags = existing_tags_response ? existing_tags_response[0] : [];
        initial_tag_ids = [];
        for(var i=0; i < existing_tags.length; i++) {
            initial_tag_ids.push(existing_tags[i].id);
            remns.postTags.push({status: 'existing', value: existing_tags[i].id})
        }
        $('#add-tags').selectize(
            {
                options: all_tags,
                items: initial_tag_ids, 
                labelField: 'name',
                searchField: 'name',
                valueField: 'id',
                highlight: false,
                create: true,
                closeAfterSelect: true,
                onItemAdd: function(d) {
                    for(var i=0; i < remns.existingTags.length; i+=1) {
                        var option = remns.existingTags[i];
                        if(option.id === parseInt(d)) {
                            remns.postTags.push({
                                "value": option.id,
                                "status": 'existing'

                            });
                            return;
                        }
                   } 
                   remns.postTags.push({
                    "value": d,
                    "status": "created"
                   });
            },
            onItemRemove: function(d) {
                for(var i=0; i< remns.postTags.length; i+=1) {
                    var addedTag = remns.postTags[i];
                    if(addedTag.value === d || addedTag.value === parseInt(d)) {
                        var temp = remns.postTags.splice(i);
                        remns.postTags = remns.postTags.concat(temp.splice(1, temp.length));
                        return;
                    }
                }
            },
            render: {
                item: function(data, escape) {
                    console.log('hitting render!');
                    console.log(data);
                    return '<div class="btn btn-small blue" >' + data.name + '</div>';
                }
            }});
        remns.existingTags = all_tags; 
    });
};
