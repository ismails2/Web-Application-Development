
const opener = document.getElementById("open-button");


const closer = document.getElementById("close-btn");

opener.addEventListener("click", function(  ) {
    document.getElementById("myForm").style.display = "block";
  }, false);
  
closer.addEventListener("click", function( ) {
    document.getElementById("myForm").style.display = "none";
}, false);