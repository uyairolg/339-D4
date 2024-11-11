// clock
function displayDateTime() {
    const dateTime = new Date();
    document.getElementById("dateTime").innerText = dateTime.toLocaleString();
}

setInterval(displayDateTime, 1000); 

