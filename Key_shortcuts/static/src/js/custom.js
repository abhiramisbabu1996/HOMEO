openerp.Key_shortcuts = function (jQuery) {
//    $(document).bind('keydown', 'f2', function assets() {
////        window.location.href = window.location.protocol + '//' + window.location.host + '/' + 'web?debug=1#view_type=form&model=account.invoice&menu_id=441&action=395';
//        window.location.href = window.location.protocol + '//' + window.location.host + '/' + 'web?debug=1#view_type=form&model=account.invoice&action=395';
//    setTimeout(function(){
//    $('button.oe_button.oe_form_button_create').click();
//}, 4000)
//    });

//openerp.Key_shortcuts = function (jQuery) {
//    $(document).bind('keydown', 'f2', function assets() {
//
//    $.when(function(){
//
//
//      window.location.assign("https://www.w3schools.com")
//
////            window.location.href = window.location.protocol + '//' + window.location.host + '/' + 'web?debug=1#view_type=form&model=account.invoice&menu_id=441&action=395';
//    }).done(function(){
//            $('button.oe_button.oe_form_button_create').click();
//
//    });
//





////
//$.ctrl = function(key, callback, args) {
//    $(document).keydown(function(e) {
//        if(!args) args=[]; // IE barks when args is null
//        console.log(e.keyCode)
//        if((e.keyCode == key.charCodeAt(0) || e.keyCode == key) && e.ctrlKey) {
//            callback.apply(this, args);
//            return false;
//        }
//    });
//};
//
//
$.shortcut = function(key, callback, args) {
    $(document).keydown(function(e) {
        if(!args) args=[]; // IE barks when args is null
        console.log(e.keyCode)
        if((e.keyCode == key.charCodeAt(0) || e.keyCode == key)) {
            callback.apply(this, args);
            return false;
        }
    });
};
//console.log('1');
//    $.ctrl('13', function() {
//        $('.oe_form_button_create').each(function() {
//            if($(this).parents('div:hidden').length == 0){
//                $(this).trigger('click');
//            }
//        });
//        $('.oe_list_add').each(function() {
//            if($(this).parents('div:hidden').length == 0){
//                $(this).trigger('click');
//            }
//        });
//    });
//console.log('2');

    $.shortcut('113', function() {
	$('.oe_form_button_create').each(function() {
		if($(this).parents('div:hidden').length == 0){
			$(this).trigger('click');
		}
	});
	$('.oe_list_add').each(function() {
            if($(this).parents('div:hidden').length == 0){
                $(this).trigger('click');
            }
        });
});
//console.log('f3');

//    ROBIN'S CODE
    $( document ).ready(function() {
    //For adding class to html tag
    var newClass = window.location.href;
    newClass = newClass.substring(newClass.indexOf('&action=') + 1).replace('=', '-num');
    $('html').addClass(newClass);
    // For adding tr to supplier table

    });
    $("button.oe_button.oe_list_add").on('click', function() {
        $('.oe_notebook_page.ui-tabs-panel.ui-widget-content .abhi_custom .oe_form_field .oe_view_manager_wrapper .oe_view_manager_body .oe_view_manager_view_list table.oe_list_content > tbody:last-child').append('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
    });

//    $( "oe_button oe_form_button_create" ).click(function() {
    $("button.oe_button.oe_form_button_create").on('click', function() {
//    alert( "Handler for .click() called." );
      $('.oe_notebook_page.ui-tabs-panel.ui-widget-content .abhi_custom .oe_form_field .oe_view_manager_wrapper .oe_view_manager_body .oe_view_manager_view_list table.oe_list_content > tbody:last-child').append('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');

    });

//END

};