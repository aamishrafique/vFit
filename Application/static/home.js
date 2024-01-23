// Slider Pagination
var ang = 0;

$("#prev").click(function () {
  ang = ang + 36;
  $("*").css("--ang", ang);
});

$("#next").click(function () {
  ang = ang - 36;
  $("*").css("--ang", ang);
});

// Robot
$(document).ready(function () {
  animateDiv($(".character"));
});

function makeNewPosition($container) {
  var h = $container.height() - 10;
  var w = $container.width() - 10;
  var nh = Math.floor(Math.random() * h);
  var nw = Math.floor(Math.random() * w);
  return [nh, nw];
}

function calculateSpeed(prev, next) {
  var x = Math.abs(prev[1] - next[1]);
  var y = Math.abs(prev[0] - next[0]);
  var greatest = x > y ? x : y;
  var speedModifier = 0.1;
  var speed = Math.ceil(greatest / speedModifier);
  return speed;
}

function animateDiv($target) {
  var next = makeNewPosition($target.parent());
  var previous = $target.offset();
  var speed = calculateSpeed([previous.top, previous.left], next);

  $target.animate({ top: next[0], left: next[1] }, speed, function () {
    animateDiv($target);
  });
}

// Dialog Box
var dialogElement = document.getElementById("dialog");

document.addEventListener("keydown", function (event) {
  if (event.key === "t") {
    updateDialogText();
  }
});

// Update the Dialog Text
function updateDialogText() {
  var box = setTimeout(function () {
    dialogElement.style.display = "block";
  }, 0);

  var one = setTimeout(function () {
    dialogElement.querySelector("p").innerText =
      "Swipe back and forth to\nchange your shirt.";
  }, 0);

  var hideTimeout = setTimeout(function () {
    closeDialog();
  }, 6000);
}
