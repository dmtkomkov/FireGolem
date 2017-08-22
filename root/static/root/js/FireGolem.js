$(document).ready(function() {
    $('.panel').on('shown.bs.collapse', function () {
        post = $('[aria-expanded=true]');
        post_id = post.attr('post-id');
        post_title = post.find('.post-title')[0].innerText;
        post_body = post.find('.post-body')[0].innerText;

        $('input.hidden[name="post_id"]').attr('value', post_id);
        $('input.post-title[name="title"]').attr('value', post_title);
        $('textarea.post-body[name="body"]').val(post_body);
    });
});