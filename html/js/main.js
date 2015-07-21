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

    var sel = document.getElementById('folder_select_container');
    sel.innerHTML = "";
    console.log(data);
    var a = document.createElement('a');
    var br = document.createElement('br');
    var folder = data[0]['above'];
    //a.innerHTML = data[0]['name'];
    a.innerHTML = '..';
    a.href = "#";
    a.setAttribute("folder", folder);
    a.onclick = function() {
        selected_folder(this);
    };
    sel.appendChild(a);
    sel.appendChild(br);


    for(var i = 1; i < data.length; i++) {
        var a = document.createElement('a');
        var br = document.createElement('br');
        var folder = data[i]['full']
        var name = data[i]['name']
        a.innerHTML = name;
        a.href = "#";
        a.value = folder;
        a.setAttribute("folder", folder);
        a.onclick = function() {
            selected_folder(this);
        };
        console.log(folder);

        //opt.innerHTML = data[i]['name'];
        //opt.value = data[i]['full'];
        sel.appendChild(a);

        var a = document.createElement('a');
        a.innerHTML = 'ADD';
        a.setAttribute("action", folder);
        a.setAttribute("action_name", name);
        a.setAttribute("action_type", data[i]['action_type']);
        a.href = "#";
        a.value = folder;
        a.setAttribute("folder", folder);
        a.onclick = function() {
            add_element_to_action_list(this);
        };

        sel.appendChild(a);
        sel.appendChild(br);



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
    console.log(element);
    var text = element.text;
    var val = element.value;
    var $li = $("<li class='ui-state-default'/>")
    var action_name = element.getAttribute("action_name");
    var action = element.getAttribute("action");
    var action_type = element.getAttribute("action_type");
    $li.text(action_name);
    $li.attr('value', val);

    $li.attr('action_type', action_type);
    $li.attr('action', action);

    $li.attr('action_name', action_name);

    $("#action_list").append($li);
    $("#action_list").sortable('refresh');}

function selected_folder(element) {
    var folder = element.getAttribute('folder');
    console.log(element);
    $.getJSON( "/get_folder/"+folder, function( data ) {
        //console.log(data);

        fill_folder_selection(data);
    });
}