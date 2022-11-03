openerp.Key_shortcuts = function (jQuery) {
    $(document).bind('keydown', 'f2', function assets() {
        window.location.href = window.location.protocol + '//' + window.location.host + '/' + 'web?debug=1#view_type=form&model=account.invoice&menu_id=441&action=395';
    setTimeout(function(){
    $('button.oe_button.oe_form_button_create').click();
}, 4000)
    });
//    ROBIN'S CODE
    $( document ).ready(function() {
    //For adding class to html tag
    var newClass = window.location.href;
    newClass = newClass.substring(newClass.indexOf('&action=') + 1).replace('=', '-num');
    $('html').addClass(newClass);
    // For adding tr to supplier table
    $('.oe_notebook_page.ui-tabs-panel.ui-widget-content .oe_form_field .oe_view_manager_wrapper .oe_view_manager_body .oe_view_manager_view_list table.oe_list_content > tbody:last-child').append('<tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr><tr>...</tr>');
    });
//END

};