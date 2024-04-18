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
        });

        div.appendChild(document.createTextNode(filterValue)); // Append filterValue text
        div.appendChild(closeButton); // Append the button to the div

        // Increment the counter
        counter++;

        containerDiv.appendChild(div);
    }
}

