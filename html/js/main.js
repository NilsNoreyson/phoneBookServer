function fill_playlist_selection(data) {

    var sel = document.getElementById('playlist_select');
    for(var i = 0; i < data.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = data[i];
        opt.value = data[i];
        sel.appendChild(opt);
    }
}




$.getJSON( "get_playlists", function( data ) {
    console.log(data.length)
    fill_playlist_selection(data);
    });

 $.ajax({
    type: "GET",
    url: "get_phonebook",
      success: function(data){

             $("#phonebook").html(data);
           }
    });


function selected_item() {
    var selectedValue = document.getElementById('playlist_select').value;
    console.log(selectedValue);
    $.getJSON( "ls_mpd/"+selectedValue, function( data ) {
        console.log(data)
        fill_playlist_selection(data);
    });
}

    $.getJSON( "ls_mpd/"+'Spotify', function( data ) {
        console.log(data.length)
        fill_playlist_selection(data);
    });