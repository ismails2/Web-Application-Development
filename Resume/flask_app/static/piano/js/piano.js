const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
                87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
                83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
                69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
                68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
                70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
                84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
                71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
                89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
                72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
                85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
                74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
                75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
                79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
                76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
                80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
                186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};

/**
 * Functionality for hovering over the keys
 */
const test = document.getElementById("keys");
const text = document.getElementsByClassName("notes");

test.addEventListener("mouseover", function( event ) {
  for (var i=0; i<text.length; i++) {
    text[i].style.opacity = "100%";
  }
}, false);

test.addEventListener("mouseout", function( event ) {
    for (var i=0; i<text.length; i++) {
        text[i].style.opacity = "0%";
    }
  }, false);

/**
 * Functionality for the when keys are played and
 * the string "weseeyou" is played
 */

var collection = '';
const allKeys = document.getElementsByClassName("key");
const img = document.getElementById("awoken");

document.addEventListener('keydown', logKey);
document.addEventListener('keydown', logKeyOther);

document.addEventListener('keydown', logKeyOt);

function logKeyOt(e) {

  var audioObj = new Audio(sound[e.keyCode]);
  audioObj.play();
}
  


function logKeyOther(e) {
  if (collection.includes('WESEEYOU'))
  {
      test.style.display = "none"
      img.style.display = "inline-block";
      var audioOther = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
      audioOther.play();
      document.removeEventListener('keydown', logKey);
  }
}
  
function logKey(e) {
  var num;
  for (var i=0; i<allKeys.length; i++) 
  {
      if (e.keyCode == allKeys[i].getAttribute("data-key"))
      {
          allKeys[i].style.background = "red";
          num = i;
          collection += e.code[3];
      }
  }

  setTimeout(function() {
      if(allKeys[num].getAttribute('id')[0] == 'b')
      {
        allKeys[num].style.background = "black";
      }
      else{
        allKeys[num].style.background = "white";
      }
    }, 500);
}