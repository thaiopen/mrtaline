
//############### Create Marker Function ##############
function create_marker(map,MapPos, MapTitle, MapDesc,  InfoOpenDefault, DragAble, Removable, iconPath)
{	  	  		  
   
    //new marker
    var marker = new google.maps.Marker({
        position: MapPos,
        map: map,
        draggable:DragAble,
        animation: google.maps.Animation.DROP,
        title:"Hello World!",
        icon: iconPath
    });

    //Content structure of info Window for the Markers
    var contentString = $('<div class="marker-info-win">'+
            '<div class="marker-inner-win"><span class="info-content">'+
            '<h1 class="marker-heading">'+MapTitle+'</h1>'+
            MapDesc+ 
            '</span><button name="remove-marker" class="remove-marker btn btn-danger btn-block  btn-xs" title="Remove Marker">Remove Marker</button>'+
            '</div></div>');	


    //Create an infoWindow
    var infowindow = new google.maps.InfoWindow();
    //set the content of infoWindow
    infowindow.setContent(contentString[0]);

    //Find remove button in infoWindow
    var removeBtn 	= contentString.find('button.remove-marker')[0];
    var saveBtn 	= contentString.find('button.save-marker')[0];

    //add click listner to remove marker button
    google.maps.event.addDomListener(removeBtn, "click", function(event) {
        remove_marker(marker);
    });

    if(typeof saveBtn !== 'undefined') //continue only when save button is present
    {
        //add click listner to save marker button
        google.maps.event.addDomListener(saveBtn, "click", function(event) {
            var mReplace = contentString.find('span.info-content'); //html to be replaced after success
            var mName = contentString.find('input.name')[0].value; //name input field value
            var mUser = contentString.find('input.user')[0].value; //name input field value
            var mDesc  = contentString.find('textarea.desc')[0].value; //description input field value
            var mType = contentString.find('select.type')[0].value; //type of marker
            var mToken = contentString.find('input[name=csrfmiddlewaretoken]')[0].value;
            token = mToken;
            if(mName =='' || mDesc =='')
            {
                alert("Please enter Name and Description!!");
            }else{
                save_marker(marker, mName, mDesc, mType, mReplace, mToken, mUser); //call save marker function
            }
        });
    }

    //add click listner to save marker button		 
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map,marker); // click on marker opens info window 
    });

    if(InfoOpenDefault) //whether info window should be open by default
    {
        infowindow.open(map,marker);
    }
}

//############### Remove Marker Function ##############
function remove_marker(Marker)
{
    //alert(token);
    /* determine whether marker is draggable 
       new markers are draggable and saved markers are fixed */
    if(Marker.getDraggable()) 
    {
        Marker.setMap(null); //just remove new marker
    }
    else
    {
        //Remove saved marker from DB and map using jQuery Ajax
        var mLatLang = Marker.getPosition().toUrlValue(); //get marker position
        var myData = {del : 'true', latlng : mLatLang, csrfmiddlewaretoken: token}; //post variables
        $.ajax({
            type: "POST",
            url: "remove_marker/",
            data: myData,
            success:function(data){
                Marker.setMap(null); 
            },
            error:function (xhr, ajaxOptions, thrownError){
                alert(thrownError); //throw any errors
            }
        });
    }

}

//############### Save Marker Function ##############
function save_marker(Marker, mName, mAddress, mType, replaceWin, mToken, mUser)
{
    //Save new marker using jQuery Ajax
    var mLatLang = Marker.getPosition().toUrlValue(); //get marker position
    var myData = {name : mName,
                  address : mAddress,
                  latlng : mLatLang,
                  report_type : mType,
                  csrfmiddlewaretoken: mToken,
                  user: mUser,
                  }; //post variables
    //console.log(replaceWin);
    console.log(myData);
    $.ajax({
        url: "/p/save_marker/",
        type: "POST",
        data: myData,
        success:function(data){
            result =  '<p>name:' + data.name + '</p>'
            result += '<p>latlng:'+ data.latlng +'</p>'
            result += '<p>desc:' + data.address+ '</p>'
            replaceWin.html(result+'<br/>'); //replace info window with new html
            Marker.setDraggable(false); //set marker to fixed
            Marker.setIcon('/static/assets/icons/pin_blue.png');//replace icon
            html = '<li><a href="#"><i class="icon-gear"></i>&nbsp; Point</a></li>';
            //:nth-child   1-index  li:eq(1)  0-index   
            p = $('#slidein-panel  ul:nth-child(2)');
            var detail = '<article class="row">'+
            '<div class="col-md-12 col-sm-12">' +
              '<div class="panel panel-default arrow left">'+
                '<div class="panel-body">'+
                  '<header class="text-left">'+
                    '<div class="comment-user"><i class="fa fa-user"></i>'+ data.name  +'</div>'+
                    '<span class="glyphicon glyphicon-time"></span><small> '+Date(data.created) +'</small><br/>'+
                    '<span class="glyphicon glyphicon-map-marker"></span><small> '+data.latlng +'</small>'+
                  '</header>'+
                  '<div class="comment-post">'+
                  '  <p> '+ data.address +'</p>'+
                  '</div>'+
                  '<p class="text-right list">'+
                  '          <a href="#" class="btn btn-xs btn-default"><span class="glyphicon glyphicon-comment"></span> Message</a>'+
                  '          <a href="#" class="btn btn-xs btn-default"><span class="glyphicon glyphicon-heart"></span> Favorite</a>'+
                  '          <a href="#" class="btn btn-xs btn-default"><span class="glyphicon glyphicon-ban-circle"></span> Unfollow</a>'+
		  '</p>'+
                '</div>'+
              '</div>'+
            '</div>'+
          '</article>'
            p.prepend(detail);
        },
        error:function (xhr, ajaxOptions, thrownError){
            alert(thrownError); //throw any errors
        }
    });
}
