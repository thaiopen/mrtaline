

// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see a blank space instead of the map, this
// is probably because you have denied permission for location sharing.


$(document).ready(function() {
     $.SlidePanel();
    var mapCenter = new google.maps.LatLng(13.736717, 100.523186); //Google map Coordinates
    var map;
    var token;
    var point = $('#slidein-panel  ul');
   
    map_initialize(); // initialize google map
    //############### Google Map Initialize ##############
    function map_initialize()
    {
        
        var googleMapOptions = 
        { 
            center: mapCenter, // map center
            zoom: 14, //zoom level, 0 = earth view to higher value
            maxZoom: 18,
            minZoom: 10,
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL //zoom control size
            },
            scaleControl: true, // enable scale control
            mapTypeId: google.maps.MapTypeId.ROADMAP // google map type
        };

        map = new google.maps.Map(document.getElementById("map-canvas"), googleMapOptions);			

        //Load Markers from the XML File, Check (map_process.php)
        $.get("map_process.php", function (data) {
            $(data).find("marker").each(function () {
                var name 		= $(this).attr('name');
                var address 	= '<p>'+ $(this).attr('address') +'</p>';
                var type 		= $(this).attr('type');
                var point 	= new google.maps.LatLng(parseFloat($(this).attr('lat')),parseFloat($(this).attr('lng')));
                create_marker(point, name, address, false, false, false, "http://sanwebe.com/assets/google-map-save-markers-db/icons/pin_blue.png");
            });
        });	

        //Right Click to Drop a New Marker
        google.maps.event.addListener(map, 'click', function(event) {
            //Edit form to be displayed with new marker
            var EditForm = $(".save-form").clone().show()[0]; 
            //Drop a new Marker with our Edit Form
            create_marker(map,event.latLng, 'New Marker', EditForm.outerHTML, true, true, true, "/static/assets/icons/pin_green.png");
        });

    }


});
