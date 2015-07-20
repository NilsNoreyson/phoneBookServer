function fill_playlist_selection(data) {

    var sel = document.getElementById('playlist_select');
    for(var i = 0; i < data.length; i++) {
        console.log(data[i]);
        var opt = document.createElement('option');
        opt.innerHTML = data[i]['playlist'];
        opt.value = data[i]['playlist'];
        sel.appendChild(opt);
    }
}

function fill_folder_selection(data) {

    var sel = document.getElementById('folder_select');
    var length = sel.options.length;
    for (i = 0; i < length; i++) {
      sel.options[i] = null;
    }
    for(var i = 0; i < data.length; i++) {
        console.log(data[i]);
        var opt = document.createElement('option');
        opt.innerHTML = data[i]['name'];
        opt.value = data[i]['full'];
        sel.appendChild(opt);
    }
}



$.getJSON( "/get_playlists/", function( data ) {
    console.log(data.length)
    fill_playlist_selection(data);
    });


$.getJSON( "/get_folder/", function( data ) {
    console.log(data);
    fill_folder_selection(data);
});


 $.ajax({
    type: "GET",
    url: "get_phonebook",
      success: function(data){

             $("#phonebook").html(data);
           }
    });


function selected_item() {
    var selectedValue = document.getElementById('folder_select').value;
    console.log(selectedValue);
    $.getJSON( "/get_folder/"+selectedValue, function( data ) {
        console.log(data);
        fill_folder_selection(data);
    });
}

