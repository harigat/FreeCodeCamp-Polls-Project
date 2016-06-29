$(document).ready(function(){
	var form_count = $('#id_choicef-TOTAL_FORMS').val();
	$('#add_form').on('click',function() {
    var formm= $("#empty_form").html().replace(/__prefix__/g, form_count);
    $(formm).css('display','none').insertBefore('#empty_form').slideDown(300);
    form_count++;
    $('#id_choicef-TOTAL_FORMS').val(form_count);});
	}
)
