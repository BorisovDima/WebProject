
(function( $ ) {

var proto = $.ui.autocomplete.prototype,
	initSource = proto._initSource;

function filter( array, term ) {
	var matcher = new RegExp( $.ui.autocomplete.escapeRegex(term), "i" );
	return $.grep( array, function(value) {
		return matcher.test( $( "<div>" ).html( value.label || value.value || value ).text() );
	});
}

$.extend( proto, {
	_initSource: function() {
		if ( this.options.html && $.isArray(this.options.source) ) {
			this.source = function( request, response ) {
				response( filter( this.options.source, request.term ) );
			};
		} else {
			initSource.call( this );
		}
	},

	_renderItem: function( ul, item) {
		return $( "<li></li>" )
			.data( "item.autocomplete", item )
			.append( $( "<a></a>" )[ this.options.html ? "html" : "text" ]( item.label ) )
			.appendTo( ul );
	}
});

})( jQuery );


$("#id_input").on('keyup', function(e){
        var value = $(this).val();
        if (value && e.which == 13) {
            window.location.replace('/search/?q=' + value );
        }
        else {
            $.ajax({
                url: '/api/autocomplete/',
                data: {'value': value},
                dataType: 'json',
                success: function (data) {
                    list = data.list;
                    $("#id_input").autocomplete({
                        source: list,
                        minLength: 2,
                        html: 'html',
                        select: function( event, ui ) {
                            login = ui.item['login']
                            $("#form-search").html('<input class="form-control mr-sm-2 pr-5">')
                            window.location.pathname = '/p/' + login + '/'
                        },
                    })
                }
            })
        }
});