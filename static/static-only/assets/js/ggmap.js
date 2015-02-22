

// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see a blank space instead of the map, this
// is probably because you have denied permission for location sharing.


$(document).ready(function() {
  var map;
  initialize();
  function initialize() {
    var position = [13.736717, 100.523186]
    var latlng = new google.maps.LatLng(position[0], position[1]);
    var mapOptions = {
      zoom: 12,
      center: new google.maps.LatLng(position[0], position[1])
  
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
    //marker = new google.maps.Marker({
    //    position: latlng,
    //	map: map,
    //	draggable: true,
    //	title: "Your current location!"
    //});

// Drawing

  var drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.MARKER,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.MARKER,
        google.maps.drawing.OverlayType.CIRCLE,
        google.maps.drawing.OverlayType.POLYGON,
        google.maps.drawing.OverlayType.POLYLINE,
        google.maps.drawing.OverlayType.RECTANGLE
      ]
    },
    markerOptions: {
      icon: "/static/assets/icons/pin_green.png",
      draggable: true
    },
    circleOptions: {
      fillColor: '#ffff00',
      fillOpacity: 1,
      strokeWeight: 5,
      clickable: false,
      editable: true,
      zIndex: 1
    }
  });
  drawingManager.setMap(map);
    //event listener that does the following after user draws point on the map
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function (point)
    {
        //"clone" the save-form to put in the infowindow
        var form =    $(".save-form").clone().show();
        var infowindow_content = form[0];
        var infowindow = new google.maps.InfoWindow({
            content: infowindow_content
        });
 
        //make each marker clickable
        google.maps.event.addListener(point.overlay, 'click', function() {
            infowindow.open(map,point.overlay);
        });
 
        //open infowindow by default
        infowindow.open(map,point.overlay);
 
        //when user clicks on the "submit" button
        form.submit({point: point}, function (event) {
            //prevent the default form behavior (which would refresh the page)
            event.preventDefault();
 
            //put all form elements in a "data" object
            var data = {
                name: $("input[name=name]", this).val(),
                description: $("textarea[name=description]", this).val(),
                category: $("select[name=category]",this).val(),
                lat: event.data.point.overlay.getPosition().lat(),
                lon: event.data.point.overlay.getPosition().lng()
            };
            trace(data)
 
            //send the results to the PHP script that adds the point to the database
            $.post("adddata.php", data, up206b.saveStopResponse, "json");
 
            //Erase the form and replace with new message
            infowindow.setContent('done')
            return false;
        });
    });
  
    // Try HTML5 geolocation
    if(navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
	var pos = new google.maps.LatLng(position.coords.latitude,
					 position.coords.longitude);
  
	var infowindow = new google.maps.InfoWindow({
	  map: map,
	  position: pos,
	  content: 'Location found using HTML5.'
	});
  
	map.setCenter(pos);
      }, function() {
	handleNoGeolocation(true);
      });
    } else {
      // Browser doesn't support Geolocation
      handleNoGeolocation(false);
    }
  }

  function handleNoGeolocation(errorFlag) {
    if (errorFlag) {
      var content = 'Error: The Geolocation service failed.';
    } else {
      var content = 'Error: Your browser doesn\'t support geolocation.';
    }
  
    var infowindow = new google.maps.InfoWindow(options);
    map.setCenter(options.position);
  }


});



