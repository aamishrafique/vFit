// Slider Pagination
var ang = 0;
var count = 0;

$("#prev").click(function () {
  ang = ang + 36;
  $("*").css("--ang", ang);
  count++;
  document.getElementById("scroll").play();
  checkAndUpdateDialogText();
});

$("#next").click(function () {
  ang = ang - 36;
  $("*").css("--ang", ang);
  count++;
  document.getElementById("scroll").play();
  checkAndUpdateDialogText();
});

document.addEventListener("keydown", function (event) {
  if (event.key === "p") {
    window.location.href = "/trigger/p";
  }
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

// document.addEventListener("keydown", function (event) {
//   if (event.key === "t") {
//     updateDialogText();
//   }
// });

// Update the Dialog Text
function updateDialogText() {
  var box = setTimeout(function () {
    dialogElement.style.display = "block";
  }, 0);

  var one = setTimeout(function () {
    document.getElementById("talk4").play();
    dialogElement.querySelector("p").innerText =
      "\nSwipe right and left to\nchange your shirt.";
  }, 0);

  var hideTimeout = setTimeout(function () {
    closeDialog();
  }, 6000);
}

// Function to Check Count and Update the Dialog Text
function checkAndUpdateDialogText() {
  if (count > 2 && count < 4) {
    // Update the Text when Count is Between 2 and 4
    var one = setTimeout(function () {
      document.getElementById("talk3").play();
      dialogElement.querySelector("p").innerText =
        "\nGive a thumbs-up to put a\nshirt on.";
    }, 0);
  }
  if (count === 5) {
    // Update the Text when Count is 5
    var two = setTimeout(function () {
      document.getElementById("talk3").play();
      dialogElement.querySelector("p").innerText =
        "\nYou would look great in this!";
    }, 0);
  } else if (count === 6) {
    // Update the Text when Count is 6
    var five = setTimeout(function () {
      dialogElement.querySelector("p").innerText =
        "\nGive a thumbs-up to put a\nshirt on.";
    }, 0);
  } else if (count === 7) {
    // Update the Text when Count is 7
    var three = setTimeout(function () {
      document.getElementById("talk1").play();
      dialogElement.querySelector("p").innerText =
        "\nThat color would really make your\neyes shine!";
    }, 0);
  } else if (count > 5 && count < 12) {
    // Update the Text when Count is Between 5 and 12
    var five = setTimeout(function () {
      dialogElement.querySelector("p").innerText =
        "\nGive a thumbs-up to put a\nshirt on.";
    }, 0);
  } else if (count === 12) {
    // Update the Text when Count is 12
    var four = setTimeout(function () {
      document.getElementById("talk5").play();
      dialogElement.querySelector("p").innerText = "\nHaving trouble choosing?";
    }, 0);
  }
}

window.onload = function () {
  document.getElementById("shrink").play();
  setTimeout(function () {
    updateDialogText();
  }, 2000);
};
