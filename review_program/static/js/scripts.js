/*!
* Start Bootstrap - Landing Page v6.0.6 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/

//Function to grab the place ID of autocompleted restaurant name
document.getElementById("popup-btn").addEventListener("click", function() {
  // Initialize autocomplete inside the click event listener
  var input = document.getElementById('restaurant_name');
  var autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.addListener('place_changed', function() {
    var place = autocomplete.getPlace();
    if (place.place_id) {
      document.getElementById('place-id').value = place.place_id;
    }
  });

  // Show the popup
  var popup = document.getElementById("popup");
  popup.style.display = "block";
});

//Function to grab the reviews from Google
// function getReviews(place_id) {
//   var request = {
//     placeId: place_id,
//     fields: ['name', 'rating', 'formatted_phone_number', 'reviews']
//   };
//   var service = new google.maps.places.PlacesService(document.createElement('div'));
//   service.getDetails(request, function(place, status) {
//     if (status == google.maps.places.PlacesServiceStatus.OK) {
//       var reviews = place.reviews;
//       console.log(typeof reviews);
//     }
//   });
// }

//Page submission function

const form = document.getElementById('myForm');
const loader = document.getElementById('loader');
const result = document.getElementById('result');

form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the page from reloading
  loader.style.display = 'block'; //loading gif
  let input_data = document.getElementById('review_input').value;
  console.log(input_data);
  
  // grab the place-id
  var place_id = document.getElementById('place-id').value;
  var request = {
    placeId: place_id,
    fields: ['name', 'rating', 'formatted_phone_number', 'reviews']
  };

  //check the sentimate value of the input review
  fetch('/predict', {
    method: 'POST',
    body: input_data,
    headers: {
      'Content-Type': 'text/plain'
    }
  })
  .then((response) => response.text())
  .then(data => {
    loader.style.display = 'none';
    console.log(data);
  });
  
  //send reviews to create matplotlib graphs
  var service = new google.maps.places.PlacesService(document.createElement('div'));
  service.getDetails(request, function(place, status) {
    if (status == google.maps.places.PlacesServiceStatus.OK) {
      var reviews = place.reviews;
      if (reviews) {
        fetch('/graphs', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(reviews)
        })
        .then(function(response) {
          if (response.ok) {
            console.log('Reviews sent to Flask instance.');
          } else {
            console.error('Error sending reviews to Flask instance.');
          }
        })
        .catch(function(error) {
          console.error('Error sending reviews to Flask instance:', error);
        });
      }
    }
  });
});

// Function to close popup
const closeBtn = document.querySelector(".close");
closeBtn.addEventListener("click", function() {
  popup.style.display = "none";
});

//Function to send textarea data to flask
// function test_func () {
//   let input_data = document.getElementById('review_input').value;
//   console.log(input_data);
// }

//Function for loading image