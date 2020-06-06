
function addCurrentLocation(lat, lng){
    var dist = distance(lat, lng, gym_lat, gym_lng, "K");
    document.getElementById("odleglosc").innerHTML = dist + ' od Ciebie';
    var link = "https://www.google.com/maps/place/"+gym_lat+"+" + gym_lng;
    document.getElementById("googlemaps").href=link; 
}

navigator.geolocation.getCurrentPosition(position => addCurrentLocation(position.coords.latitude, position.coords.longitude),
           error => addCurrentLocation(52.219761, 21.002734));

function distance(lat1, lon1, lat2, lon2, unit) {
      var radlat1 = Math.PI * lat1/180
      var radlat2 = Math.PI * lat2/180
      var theta = lon1-lon2
      var radtheta = Math.PI * theta/180
      var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
      if (dist > 1) {
          dist = 1;
      }
      dist = Math.acos(dist)
      dist = dist * 180/Math.PI
      dist = dist * 60 * 1.1515
      if (unit=="K") { dist = dist * 1.609344 }
      if (unit=="N") { dist = dist * 0.8684 }
      var res = "";
      if (dist < 1) {
          res = (dist * 1000).toFixed(0) + "m";
      }
      else {
          res = dist.toFixed(2) + "km";
      }
      return res;
  }

document.getElementById("img1").src=photos[0];
document.getElementById("img2").src=photos[1];
document.getElementById("img3").src=photos[2];