//
// (c) 2017 - Tech Haven Network - Written by Brammers
//
$(document).ready(function() {

    $("#thn_form input[type=submit], #thn_form button, #thn_form a.button").button();

    if (typeof ml !== 'undefined')
    {
        if (ml.lang=='en')
        {
            $.datepicker.setDefaults( $.datepicker.regional['en-GB']);
        }
        else
        {
            $.datepicker.setDefaults( $.datepicker.regional[ml.lang]);
        }
    }
    else
    {
        $.datepicker.setDefaults( $.datepicker.regional['en-GB']);
    }

    $("#thn_form .thn_date_picker").datepicker({ dateFormat: 'dd/mm/yy', minDate:new Date(2012,8,23),  maxDate: "+0D"  });

    if ( $( "#thn_search_form" ).length)
    {
        var o = $('#thn_search_form_link').offset();
        var h = $('#thn_search_form_link').height();

        $('#thn_search_form').css({ 'top': o.top+h,
            'left': o.left
        });

        $('#thn_search_form_link').click(function() {
            $('#thn_search_form').fadeToggle("fast", "linear");
            return false;
        });

        $('#thn_search_form_close').click(function() {
            $('#thn_search_form').hide();
            return false;
        });
    }

});