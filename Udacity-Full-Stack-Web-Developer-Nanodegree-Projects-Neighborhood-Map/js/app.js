var initialLocations;
var map;
    
var defaultIcon;
var highlightedIcon;
var viewmodel;
var infoWindow;



var Location = function(data) {
	var self = this;
	this.name = data.name;
	this.lat = data.gtfs_latitude;
	this.lng = data.gtfs_longitude;

	this.visible = ko.observable(true);

    defaultIcon = makeMarkerIcon('0091ff');
    highlightedIcon = makeMarkerIcon('FFFF24');
    
	this.marker = new google.maps.Marker({
			position: new google.maps.LatLng(this.lat, this.lng),
			map: map,
			title: data.name,
            animation: google.maps.Animation.DROP,
            icon: defaultIcon
	});
    
	this.showMarker = ko.computed(function() {
		if(this.visible() === true) {
			this.marker.setMap(map);
		} else {
			this.marker.setMap(null);
		}
		return true;
	}, this);

	this.marker.addListener('click', function() {
         self.clickMarker();
    });
    
    this.marker.addListener('mouseover', function() {
         this.setIcon(highlightedIcon);
    });
    
    this.marker.addListener('mouseout', function() {
         this.setIcon(defaultIcon);
    });
    
    this.clickMarker = function() {
		map.setZoom(11);
        map.setCenter(self.marker.position);
        
		var contentString = '<div class="info-window-content"><div class="name"><b>' + data.name + "</b></div>" + '<div class="address"><b>' + data.address + "</b></div></div>";
        populateInfoWindow(self.marker, contentString);
        
        self.marker.setAnimation(google.maps.Animation.BOUNCE);
      	setTimeout(function() {
      		self.marker.setAnimation(null);
     	}, 2100);
        
	};

};

var ViewModel = function() { 
    
	var self = this;

	this.searchTerm = ko.observable("");

	this.locationList = ko.observableArray([]);
    
    initialLocations.forEach(function(locationItem){
		self.locationList.push(new Location(locationItem));
	});
	
	this.filteredList = ko.computed( function() {
		var filter = self.searchTerm().toLowerCase();
		if (!filter) {
			self.locationList().forEach(function(locationItem){
				locationItem.visible(true);
			});
			return self.locationList();
		} else {
			return ko.utils.arrayFilter(self.locationList(), function(locationItem) {
				var string = locationItem.name.toLowerCase();
				var result = (string.search(filter) >= 0);
				locationItem.visible(result);
				return result;
			});
		}
	}, self);
    
    this.sidebarAppear = ko.observable(true);
    
    this.toggleSideBar = function() {
        this.sidebarAppear(!this.sidebarAppear());
    };
    
    this.changeLayout = ko.computed(function() {
		if(this.sidebarAppear() === true) {
            if($(window).width() <= 620){
              document.getElementById('main').style.width = '50%';
              document.getElementById('side').style.width = '50%';
              document.getElementById('side').style.display = 'block';
            }
            else{
			  document.getElementById('main').style.width = '80%';
              document.getElementById('side').style.width = '20%';
              document.getElementById('side').style.display = 'block';
            }
		}
        else {
            document.getElementById('side').style.display = 'none';
			document.getElementById('main').style.width = '100%';
		}
		return true;
	}, this);
};

// helper function
function makeMarkerIcon(markerColor) {
        var markerImage = new google.maps.MarkerImage(
          'https://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
          '|40|_|%E2%80%A2',
          new google.maps.Size(21, 34),
          new google.maps.Point(0, 0),
          new google.maps.Point(10, 34),
          new google.maps.Size(21,34));
        return markerImage;
}

function populateInfoWindow(marker, contentString){
    if (infoWindow.marker != marker) {
          infoWindow.marker = marker;
          infoWindow.setContent(contentString);
          infoWindow.open(map, marker);
          // Make sure the marker property is cleared if the infowindow is closed.
          infoWindow.addListener('closeclick', function() {
            infoWindow.marker = null;
            map.setZoom(10);
            map.setCenter({lat: 37.803768, lng: -122.271450});
          });
    }
}

//when window resize conditionals are met (when no API error)
function resetMap() {
        var windowWidth = $(window).width();
        if(windowWidth <= 620){
              viewmodel.sidebarAppear(false);
        }
    
        if(windowWidth <= 767) {
            map.setCenter({lat: 37.803768, lng: -122.083450});
            map.setZoom(9);
        }
        else{
            map.setCenter({lat: 37.803768, lng: -122.071450});
            map.setZoom(10);
        }  
}

// //when window resize conditionals are met (exist API error)
function resetMapWithApIError() {
        var windowWidth = $(window).width();
        if(windowWidth <= 700){
               document.getElementById('title').style.fontSize = '14px';
        }
        else{
               document.getElementById('title').style.fontSize = '28px';
        }  
}

function startApp() {
    
    map = new google.maps.Map(document.getElementById('map'), {
			zoom: 10,
			center: {lat: 37.803768, lng: -122.071450}
	});
    
    infoWindow = new google.maps.InfoWindow();
    
    $.getJSON('https://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y').done(function(data) {
        // get all bart station information from returned data
        initialLocations = data.root.stations.station;
        
        viewmodel = new ViewModel(); 
        ko.applyBindings(viewmodel);
        
        $(window).resize(function() {
        resetMap();
    });
	}).fail(function() {
		alert("There was an error with the Bart API call. Please refresh the page and try again to load Bart data.");
        
        $(window).resize(function() {
            resetMapWithApIError();
        });
	});
}
    
 

var errorhandler = function() {
	   alert("Google Maps has failed to load. Please check your internet connection and try again.");
        $(window).resize(function() {
            resetMapWithApIError();
        });   
};
