function fill_playlist_selection(data) {

    var sel = document.getElementById('playlist_select');
    for(var i = 0; i < data.length; i++) {
        //console.log(data[i]);
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
        //console.log(data[i]);
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
    var element = document.getElementById('folder_select')
    var selectedValue = document.getElementById('folder_select').value;
    var selectedElement = element.options[element.selectedIndex];
    console.log(selectedElement);
    $.getJSON( "/get_folder/"+selectedValue, function( data ) {
        //console.log(data);
        add_element_to_action_list(selectedElement);
        fill_folder_selection(data);
    });
}

  $(function() {
    $( "#action_list" ).sortable();
    $( "#action_list" ).disableSelection();
  });


 function add_element_to_action_list(element){
    console.log(element.value);
    var text = element.text;
    var val = element.value;
    var $li = $("<li class='ui-state-default'/>")
    $li.text(text);
    $li.attr('value', val);
    $li.attr('type', 'folder');

    $("#action_list").append($li);
    $("#action_list").sortable('refresh');}