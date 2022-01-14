// init

//add event listener on document ready
document.addEventListener('DOMContentLoaded', function fetchData() {
    fetch('http://localhost:8282/')
        .then(response => response.json())
        .then(data => {
        //    create a card for each item
            parentElement = '#featured-div';
            data.forEach(item => {
                createCard(item, parentElement);
            });
        })
        .catch(error => console.log(error));
});


function createCard(item, parentElement) {
    const card = document.createElement('div');
    card.classList.add("box");
    card.innerHTML = `
           <ul class="collection">
                <li class="collection-item">
                    <h5>${item.name}</h5>
                </li>
                <li class="collection-item">
                    <p>Branch: ${item.branch}</p>
                </li>
                <li class="collection-item">
                    <p>${item.city}</p>
                </li>
                <li class="collection-item">
                    <p>Kifle-Ketema: ${item.kifle_ketema}</p>
                </li>
                <li class="collection-item">
                    <p>Direction: ${item.direction}</p>
                 </li>
                <li class="collection-item">
                    <p>Building: ${item.building}</p>
                </li>
                <li class="collection-item">
                    <p>Flat: ${item.flat}</p>
                </li>
                <li class="collection-item">
                    <p>Phone: ${item.phone}</p>
                </li>

            </ul>`;

    //add the card to the DOM
    document.querySelector(parentElement).appendChild(card);
}



//add event for the search button
document.querySelector('#search-btn').addEventListener('click', function (e) {
    //get the value of the search input
    e.preventDefault();
    const searchValue = document.querySelector('#q').value;
    //fetch the data from the server
    parentElement = '#search-result-div';
    fetch('http://localhost:8282/contacts/search?q=' + searchValue)
        .then(response => response.json())
        .then(data => {
            //clear the featured div
            document.querySelector('#search-result-div').innerHTML = '';
            console.log(data);  
            //create a card for each item
            data.forEach(item => {
                createCard(item, parentElement);
            });
        }).catch(error => console.log(error));
});


