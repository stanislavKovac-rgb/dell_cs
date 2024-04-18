const tableDropdown = document.getElementById('tableDropdown');
const tableData = document.getElementById('tableData');

tableDropdown.addEventListener('change', function() {
  const selectedTable = this.value;
  fetchTableData(selectedTable);
});

function fetchTableData(table, filterValue = "") { // Optional filterValue parameter
  const url = 'http://127.0.0.1:5000/get_data'; // Replace with your actual URL for the Python script (if different)
  const data = { table: table };

  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: { 'Content-Type': 'application/json' }
  })
  .then(response => response.json())
  .then(data => {
    // Filter data based on filterValue (lowercase for case-insensitive filtering)
    const filteredData = filterValue !== "" ? data.filter(row => {
      for (const value in row) {
        if (String(row[value]).toLowerCase().includes(filterValue.toLowerCase())) {
          return true;
        }
      }
      return false;
    }) : data; // No filter applied if filterValue is empty

    tableData.innerHTML = ''; // Clear previous data
    buildTable(filteredData);
  })
  .catch(error => {
    console.error('Error fetching data:', error);
    tableData.innerHTML = '<p>Error loading data.</p>';
  });
}


function buildTable(data) {
  // This function builds the HTML table structure based on the data received
  const table = document.createElement('table');
  const headerRow = document.createElement('tr');

  // Add table headers dynamically based on data keys
  for (const key in data[0]) {
    const headerCell = document.createElement('th');
    headerCell.textContent = key;
    headerRow.appendChild(headerCell);
  }

  table.appendChild(headerRow);

  // Add data rows (limit 100 rows)
  data.slice(0, 100).forEach(row => {
    const dataRow = document.createElement('tr');
    for (const value in row) {
      const dataCell = document.createElement('td');
      dataCell.textContent = row[value];
      dataRow.appendChild(dataCell);
    }
    table.appendChild(dataRow);
  });

  tableData.appendChild(table);
}

//adding webpage element on click
//1. Create a div and add it to webpage
let div = document.createElement("div");
div.classList.add("current-filters-el");
let containerDiv = document.querySelector(".current-filters");
containerDiv.appendChild(div);

//2. Event on submit btn
let submitBtn = document.getElementById("submitBtn");
submitBtn.addEventListener("click",displayFilterDetail);

//3. Create displayFitlerDetail
// Counter for numbered classes
let counter = 0;

// Function to remove a div
function removeDiv(divToRemove) {
    divToRemove.remove();
}

function displayFilterDetail() {
    let filterValue = document.getElementById("newfilter").value;

    // Check if filterValue is not empty
    if (filterValue !== "") {
        // Check if the container div has reached its maximum width
        if (containerDiv.scrollWidth > containerDiv.clientWidth) {
            // If the container div has overflow, insert the div on the next row
            containerDiv.appendChild(document.createElement('br'));
        }

        let div = document.createElement("div");
        div.classList.add("current-filters-el");
        div.classList.add("current-filters-el-" + counter); 
        div.style.backgroundColor = "#027bff"; 
        div.style.height = "30px"; 
        div.style.display = "flex"; 
        div.style.alignItems = "center"; 
        div.style.padding = "5px"; 
        div.style.color = "white"; 
        div.style.borderRadius = "3px"; 
        div.style.margin = "5px"; 

        // Create a button element
        let closeButton = document.createElement("button");
        closeButton.textContent = "x";
        closeButton.style.backgroundColor = "#2d3339";
        closeButton.style.color = "white";
        closeButton.style.width = "20px";
        closeButton.style.height = "20px";
        closeButton.style.marginLeft = "10px";
        closeButton.style.border = "none";
        closeButton.style.borderRadius = "10%"; 
        closeButton.style.display = "flex"; 
        closeButton.style.alignItems = "center"; 
        closeButton.style.justifyContent = "center";
        closeButton.style.fontSize = "14px"; 
        closeButton.style.cursor = "pointer";

        // Add click event listener to the button
        closeButton.addEventListener("click", function() {
            removeDiv(div);
            fetchTableData(selectedTable, filterValue = "")
            buildTable(data)
        });

        div.appendChild(document.createTextNode(filterValue)); // Append filterValue text
        div.appendChild(closeButton); // Append the button to the div

        // Increment the counter
        counter++;

        containerDiv.appendChild(div);

        const tableDropdown = document.getElementById('tableDropdown');
        const selectedTable = tableDropdown.value;

        fetchTableData(selectedTable, filterValue)
        buildTable(data)


    }
}


