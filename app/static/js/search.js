$('#tfsearch').submit(function(query) {
	var queryString = $('tftextinput').value();
	$.get("/search", {data: queryString}).done(function(data) {
		// Handle the search results
		
	});
});
