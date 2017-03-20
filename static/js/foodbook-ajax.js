//Ajax to handle the favourite function.
$(document).ready(function(){
    $("#favourite").click(function(){
        // Examines the current recipe by id.
        var recipeid = $(this).data('recipeid');
        if(($(this).html() == "Unfavourite")){
        	// If the user has already favourited, unfavourite.

        	//Make a GET request to execute the code which handles underlying models.
			$.get('/favourite/false', {recipe_id: recipeid}, function(data){
	       		$('#favourite_count').html(data);
			});
			//Change to a favourite button after unfavouriting.
			$(this).html('Favourite');

        } else {
        	// Otherwise, favourite.
	       	$.get('/favourite/true', {recipe_id: recipeid}, function(data){
	       		$('#favourite_count').html(data);
			});
			$(this).html('Unfavourite');
			
	    }
	});
});