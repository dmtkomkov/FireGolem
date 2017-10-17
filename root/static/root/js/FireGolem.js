$(document).ready(function() {
    $('.panel').on('shown.bs.collapse', function () {
        post = $('[area-expanded=true]');
        post_id = post.attr('post-id');
        post_title = post.find('.post-title')[0].innerText;
        post_body = post.find('.post-body')[0].innerText;

        $('input.hidden[name="post_id"]').attr('value', post_id);
        $('input.post-title[name="title"]').attr('value', post_title);
        $('textarea.post-body[name="body"]').val(post_body);

        $('.btn[data-target="#deletePost"]').prop('disabled', false);
        $('.btn[data-target="#editPost"]').prop('disabled', false);
    });

    $('.panel').on('hidden.bs.collapse', function () {
        if ($('[area-expanded=true]').length == 0) {
            $('.btn[data-target="#deletePost"]').prop('disabled', true);
            $('.btn[data-target="#editPost"]').prop('disabled', true);
        }
    });

    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.ajaxOptions = {type: "PUT"};

    var to_edit = ['#task-name', '#task-description', '#task-status', '#task-area', '#task-project',
                '#area-name', '#area-description', '#project-name', '#project-description'];
    for (i = 0; i < to_edit.length; i++) {
        $(to_edit[i]).editable({
            send: 'always',
        });
    }
});