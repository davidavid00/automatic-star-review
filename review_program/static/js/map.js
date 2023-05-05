let myMap = L.map("map-plot", {
  center: [-32.32, 147],
  zoom: 6
});

// Adding a tile layer (the background map image) to our map:
// We use the addTo() method to add objects to our map.
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

const url = '/api/bionet'

d3.json(url).then(function(OG_data) {

  // var dropdown1 = d3.select("#selDataset");
  // console.log(dropdown1);

  function heapmap(animalName){
    var selectedAnimalData = OG_data.filter(function(record) {
      return record.vernacularName === animalName;
    });

    console.log(selectedAnimalData);
    let heatArray = [];

    selectedAnimalData.forEach(function(record) {
      var latitude = record.latitude;
      var longitude = record.longitude;

      if (latitude) {
        //console.log(location);
        heatArray.push([latitude, longitude]);
      }
    });

    let heat = L.heatLayer(heatArray, {
      radius: 20,
      blur: 35}).addTo(myMap);
  }

// Set up the event listener for the dropdown menu
  // dropdown1.on("change", function(){
  //   var selectedAnimal = d3.select(this).property("value");
  //   UpdateMap(selectedAnimal);
  // });
  
  function UpdateMap() {
    heapmap(animalData);
}

  
});


// function heatmap(data,id){

//     let heatArray = [];

//     for (let i = 0; i < data.length; i++) {
//       let location = data[i];
//       if (location) {
//         //console.log(location);
//         heatArray.push([location.decimalLatitude, location.decimalLongitude]);
//       }

//     }

//     let heat = L.heatLayer(heatArray, {
//       radius: 20,
//       blur: 35
//     }).addTo(myMap);
//   }





// function buildMap() {
//     Plotly.d3.json('/api/bionet', function(response) {
//         console.log(response);
      
//         var layout = {
//             title: 'Map Title',
//             autosize: true,
//             width: 1000,
//             height: 600,
//             hovermode: 'closest',
//             showlegend: false,
//             geo: {
//                 scope: 'usa',
//                 projection: {type: 'albers usa'},
//                 showland: true,
//                 landcolor: 'rgb(217, 217, 217)',
//                 subunitwidth: 1,
//                 countrywidth: 1,
//                 subunitcolor: 'rgb(255,255,255)',
//                 countrycolor: 'rgb(255,255,255)'
//             },
//             responsive: true
//         };
      
//         var data = [{
//             type: 'scattergeo',
//             mode: 'markers',
//             locations: [],
//             hoverinfo: 'text',
//             marker: {
//                 size: 8,
//                 line: {
//                     color: 'rgb(8,8,8)',
//                     width: 0.5
//                 },
//                 opacity: 0.8
//             }
//         }];

//         Plotly.plot('plot', data, layout);
//     });
// }