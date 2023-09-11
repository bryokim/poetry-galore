$(document).ready(function() {
    const userId = $("DIV.user-like-details").attr("data-id");

    $.get(`/user/likes`, function(data) {
        $(`SPAN#${userId}-likes-count`).html(data.likes);
    })

    $.get(`/user/liked`, function(data) {
        $(`SPAN#${userId}-liked-count`).html(data.likes);
    })

})