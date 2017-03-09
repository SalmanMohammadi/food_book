// Handles JQuery for the foodbook app.
$(function() {
    $('recipe').hover(
        function() {
            $(this).attr("src", document.getElementById("recipeGif").value);
        },
        function() {
            $(this).attr("src", document.getElementById("recipeThumb").value);
        }                         
    );                  
});