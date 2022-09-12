function buttonClick() {
    fetch("http://localhost:5000/usersjson")
    .then((response) => response.json())
    .then((data) => showResults(data));
}

function showResults(data) {
    console.log(data);
    let results = "";
    for (const datum of data) {
        console.log(datum);
        results+="Username: " + datum.username + " Email: " + datum.email + "<br>";
    }

    document.getElementById("result").innerHTML = results;
}

function hideUsers() {
    document.getElementById("result").innerHTML = "";
}