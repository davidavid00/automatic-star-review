$(document).ready(function() {

    // Use ajax function from jQuery library to retrieve data as JSON from server endpoint /api/bionet 
    $.ajax({
        url: '/api/bionet',
        dataType: 'json',
        success: function(data) {

            // Use d3 to select the dropdown element with the id 'selDataset'
            var dropdown = d3.select("#selDataset");

            // Extract unique vernacular names from the data and sort the vernacular names alphabetically
            var vernacularNames = [...new Set(data.map(record => record.vernacularName))];
            vernacularNames.sort();

            // Iterate over each vernacular name and append an option element to the dropdown
            vernacularNames.forEach(function(name) {
                dropdown.append("option").text(name).property("value", name);
            });

            // Function to display the total number of sightings of the selected animal
            function displayTotalSightings(animalName, data) {
                // Filter the data to get records only for the selected animal
                var selectedAnimalData = data.filter(function(record) {
                    return record.vernacularName === animalName;
                });
                // Get the count of the filtered records
                var totalSightings = selectedAnimalData.length;
                // Display the count in the element with id 'totalSightings'
                if (animalName) {
                    d3.select("#totalSightings").html("Total number of sightings: <b>" + totalSightings + "</b>");
                }
            }

             // Function to display bar-chart of the total number of sightings of the selected animal per county
            function buildPlot(animalName, data) {
                // Filter the data to get records only for the selected animal
                var selectedAnimalData = data.filter(function(record) {
                return record.vernacularName === animalName;
                });
            
                // Group the filtered data by county and count the number of records for each county
                var countyCounts = {};
                selectedAnimalData.forEach(function(record) {
                var county = record.county;
                if (countyCounts[county]) {
                    countyCounts[county]++;
                    } else {
                    countyCounts[county] = 1;
                    }
                });
            
            // Convert the county counts object to an array of objects with keys 'county' and 'count'
            var countyCountsArray = [];
            for (var county in countyCounts) {
                countyCountsArray.push({
                    county: county,
                    count: countyCounts[county]
                });
            }
            
            // Sort the county counts array by count in descending order
            countyCountsArray.sort(function(a, b) {
                return b.count - a.count;
            });
            
            // Extract the county names and counts from the sorted county counts array
            var countyNames = countyCountsArray.map(function(obj) {
                return obj.county;
            });
            var countyCountsData = countyCountsArray.map(function(obj) {
                return obj.count;
            });
            
            // Create the plotly bar chart
            var plotData = [{
                y: countyCountsData,
                x: countyNames,
                type: 'bar',
                orientation: 'v'
            }];
            var plotLayout = {
                title: 'Total number of sightings per county',
                yaxis: {
                    title: 'Number of sightings'
                },
                xaxis: {
                    title: 'County'
                }
            };
            Plotly.newPlot('myChart', plotData, plotLayout);
            }
            function heapmap(animalName, data){
                try{
                    heatmapLayer.remove();
                    console.log('layer removed')
                }catch{
                    console.log('No map');
                }
                // if (typeof heat !== 'undefined') {
                //     // myMap.removeLayer(heat);
                //     console.log("HEAT IS HERE")
                //   }

                var selectedAnimalData = data.filter(function(record) {
                    return record.vernacularName === animalName;
                });
        
                let heatArray = [];
        
                selectedAnimalData.forEach(function(record) {                   
                    var latitude = record.decimalLatitude;
                    var longitude = record.decimalLongitude;
                    // console.log(latitude);
                    // console.log(longitude);
                    if (latitude) {
                        heatArray.push([latitude, longitude]);
                    }
                });

                heatmapLayer = L.heatLayer(heatArray, {
                    radius: 30,
                    blur: 10
                }).addTo(myMap);
            }
            // Event listener for when a new animal is selected from the dropdown
            dropdown.on("change", function() {
                // Get the value of the selected dropdown option
                var selectedAnimal = d3.select(this).property("value");
                // Call the optionChanged function with the selected animal's vernacular name
                optionChanged(selectedAnimal);
            });
            
            function optionChanged(animalName) {
                // Use ajax function from jQuery library to retrieve data as JSON from server endpoint /api/bionet 
                $.ajax({
                    url: '/api/bionet',
                    dataType: 'json',
                    success: function(data) {
                        // Call the displayTotalSightings function to display the total number of sightings of the selected animal
                        displayTotalSightings(animalName, data);
                        // Call the buildPlot function to build the plot for the selected animal
                        buildPlot(animalName, data);
                        heapmap(animalName, data);
                    },
                });
            }

            // Build the plot after the document has loaded and the necessary elements have been created

            

        },
        // Specify a callback function to handle any errors during the data retrieval process
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('Error retrieving data from server: ' + textStatus);
        }
    });
});

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
  let heatmapLayer;