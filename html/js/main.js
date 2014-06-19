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