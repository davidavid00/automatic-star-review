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
const result = document.getElementById('result');

form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the page from reloading
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
    // Update the modal title with the returned value
    var sentiment = JSON.parse(data)
    console.log(typeof sentiment);
    var sentiment_response = sentiment['prediction'];
    console.log(sentiment_response);
    updateTitle(sentiment_response);
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
        .then(response => response.json())
        .then(data=> {
          // Get the reference to the input boxes and modal body
          const restaurantNameInput = document.getElementById('restaurant_name');
          const placeIdInput = document.getElementById('place-id');
          const review_html = document.getElementById('review_input');
          const modalBody = document.querySelector('.modal-body');
          const submit_button = document.getElementById('submitButton');

          // Create image elements
          const image1 = document.createElement('img');
          image1.src = "emotions.png";
          image1.alt = 'Image 1';

          const image2 = document.createElement('img');
          image2.src = "emotions.png"; //to update with wordcloud
          image2.alt = 'Image 2';

          restaurantNameInput.remove();  // Remove restaurantNameInput element
          placeIdInput.remove();         // Remove placeIdInput element
          review_html.remove();
          submit_button.remove();
          modalBody.insertAdjacentHTML('beforebegin', '<img id="graph" src="../static/assets/img/emotions.png" alt="..." />');
          modalBody.insertAdjacentHTML('beforebegin', '<img id="graph" src="../static/assets/img/wordcloud.png" alt="..." />'); //image2
          modalBody.value
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

// Function to update modal content
function updateTitle(value) {
  // Get the modal header element
  var modalTitle = document.querySelector('.modal-title');

  // Replace the text content of the modal title
  modalTitle.textContent = "Your review was considered " + value;
}

//Function to send textarea data to flask
// function test_func () {
//   let input_data = document.getElementById('review_input').value;
//   console.log(input_data);
// }

//Function for loading image