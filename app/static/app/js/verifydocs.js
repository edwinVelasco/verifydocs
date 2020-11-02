var points = [[20, 725],[525, 725], [20, 35], [525, 35]]

function previewDocument(endpoint){
    var pos_x = $('#id_pos_x').val();
    var pos_y = $('#id_pos_y').val();
    if(pos_x<0){
        $('#pos_x_errors').html(
            '<ul class="errorlist">' +
            '<li>El valor no puede ser inferior a 0</li>' +
            '</ul>'
        )
        return;
    }
    if(pos_y<0){
        $('#pos_y_errors').html(
            '<ul class="errorlist">' +
            '<li>El valor no puede ser inferior a 0</li>' +
            '</ul>'
        )
        return
    }
    $('#pos_x_errors').html('');
    $('#pos_y_errors').html('');
    var formdata = new FormData($('#form-data').get(0));
    console.log(formdata.entries());
    $.ajax({
        url: endpoint,
        type: "POST",
        contentType: false,
        processData: false,
        data: formdata,
        success : function (response){
            $('#id_embed').attr('src', 'data:application/pdf;base64,'+response+'#zoom=40');
        }
    })
}
function defaultPosition(position, url){
    var point = points[position];
    for(var i=0; i<points.length; i++){
        if(i===position){
            $('#check_'+i).prop("checked", true);
        }else{
            $('#check_'+i).prop("checked", false);
        }

    }
    $('#id_pos_x').val(point[0]);
    $('#id_pos_y').val(point[1]);
    previewDocument(url);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');