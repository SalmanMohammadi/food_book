// Handles JQuery for the foodbook app.
$(document).ready(function(){
    $(".img").(function(){
        $(this).find(".thumb").hide();
        $(this).find(".gif").show();
    },
    function(){
        $(this).find(".thumb").show();
        $(this).find(".gif").hide();
    });
});	