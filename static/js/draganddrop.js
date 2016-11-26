var one = 0,
    two = 0,
    three = 0,
    four = 0,
    five = 0,
    six = 0,
    seven = 0,
    eight = 0;


cores = {};
cores[1] = one; 
cores[2] = two; 
cores[3] = three; 
cores[4] = four; 
cores[5] = five; 
cores[6] = six; 
cores[7] = seven; 
cores[8] = eight; 


 function _(id) {
     return document.getElementById(id);
 }
 var droppedIn = false;

 function drag_start(event) {

     event.dataTransfer.dropEffect = "move";
     event.dataTransfer.setData("text", event.target.getAttribute('id'));
 }


 function drag_drop(event) {

     event.preventDefault(); /* Prevent undesirable default behavior while dropping */
     var elem_id = event.dataTransfer.getData("text");
     event.target.appendChild(_(elem_id));
     var string_elem_id = elem_id.split(" ");
     var id_technique = string_elem_id[0];
     var number_core = string_elem_id[1];
     var name_technique = string_elem_id[2];
     _(elem_id).style.cursor = "default";
     droppedIn = true;


     if (number_core == 1) {
        one = one+1;
        cores["1"] = one;
     } else if (number_core == 2) {
        two = two+1;
        cores["2"] = two;
     } else if (number_core == 3) {
        three = three+1;
         cores["3"] = three;
     } else if (number_core == 4) {
        four = four+1;
        cores["4"] = four;
     } else if (number_core == 5) {
        five = five+1;
        cores["4"] = five;
     } else if (number_core == 6) {
        six = six+1;
        cores["6"] = six;
     } else if (number_core == 7) {
        seven = seven+1;
        cores["7"] = seven;
     } else if (number_core == 8) {
        core = cores+1;
        cores["8"] = eight;
     }

    localStorage.setItem("cores",  JSON.stringify(cores));
    get_techniqueID();


}

 function drag_end(event) {

     droppedIn = false;
 }

 function readDropZone() {
     for (var i = 0; i < _("drop_zone").children.length; i++) {
         alert(_("drop_zone").children[i].id + " QUANDO ISSO ACONTECE?");
     }
     /* Run Ajax request to pass any data to your server */
 }

function get_techniqueID () {
    var childDivs = document.getElementById('drop_zone').getElementsByTagName('div');
     var arrayTechniques = "";
        for( i=0; i< childDivs.length; i++ ){
            var string_elem_id  = childDivs[i].id.split(" ");
            var id_technique = string_elem_id[0];
            arrayTechniques = arrayTechniques + id_technique + " ";
        }
    document.getElementById("id_technique").value = arrayTechniques;
}

