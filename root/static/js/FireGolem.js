$(document).ready(function() {
    $('.panel').on('shown.bs.collapse', function () {
        post_id = $('[aria-expanded=true]').attr('post-id');
        $('[name="post_id"]').attr('value', post_id);
    });
});