function ticketPrice()
{
    var ticketPrice=0;
    var theForm = document.forms["ticketsForm"];
    var ticketNumber = theForm.elements["tickets"];
    ticketPrice=ticketNumber.value * 6;
    return ticketPrice;
}


function calculateTotal()
{
    var orderPrice = ticketPrice();
    //display the result
    var divobj = document.getElementById('totalPrice');
    divobj.style.display='block';
    divobj.innerHTML = "The total price for your tickets is £"+orderPrice+"<br>We will collect it from you when we bring your tickets to you.";
}
