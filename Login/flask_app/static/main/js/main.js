 function toggle_visibility() {
    var e = document.getElementById('feedback-main');
    if(e.style.display == 'block')
       e.style.display = 'none';
    else
       e.style.display = 'block';
 }

 const opener = document.getElementById("open-button");


const closer = document.getElementById("close-btn");

opener.addEventListener("click", function(  ) {
    document.getElementById("myForm").style.display = "block";
  }, false);
  
closer.addEventListener("click", function( ) {
    document.getElementById("myForm").style.display = "none";
}, false);