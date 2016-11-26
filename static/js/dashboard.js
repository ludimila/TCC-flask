
function sort_dict(cores_dashboard) {

    // Create items array
var items = Object.keys(cores_dashboard).map(function(key) {
    return [key, cores_dashboard[key]];
});

// Sort the array based on the second element
items.sort(function(first, second) {
    return second[1] - first[1];
});

// Create a new array with only the first 8 items
 return (items.slice(0, 8));

}


function count_using_cores(cores_dashboard_2) {

    var using_cores = 0;
    var half_percent = 0;
    var remaining_cores = 0;

    for (var i=0; i < cores_dashboard_2.length; i++){
        var make_array = cores_dashboard_2[i];

        if (make_array[1] != 0){
            using_cores++;
        }
    }
    return using_cores;
}    


