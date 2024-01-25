let isFirstLoad = true;

document.addEventListener("keydown", function (event) {
  if (event.key === " ") {
    sleepAwakeState();
    playEnterSound();
  }
  if (event.key === " " && !dialogShown) {
    showDialog();
  }
});

function sleepAwakeState() {
  const innerBody = document.querySelector(".inner");
  const jump = document.querySelector(".robot-container");
  const zzz = document.querySelector(".wake-up");
  const leftEye = document.querySelector(".robot-eye-left");
  const rightEye = document.querySelector(".robot-eye-right");
  const orb1 = document.querySelector(".orb1");
  const orb2 = document.querySelector(".orb2");

  // Check if the Robot is in Sleep Mode, then Switch to Motion, and Vice Versa
  if (innerBody.classList.contains("animate-sleep-movement")) {
    innerBody.classList.remove("animate-sleep-movement");
    innerBody.classList.add(
      "animate-wobble",
      "animate-tilt-head",
      "animate-breathe",
      "animate-look"
    );
  } else {
    innerBody.classList.remove(
      "animate-wobble",
      "animate-tilt-head",
      "animate-breathe",
      "animate-look"
    );
    innerBody.classList.add("animate-sleep-movement");
  }

  // Check if the Robot is Sleeping, then Stay, else, Jump, and Vice Versa
  if (isFirstLoad) {
    jump.classList.remove("animate-stay");
    jump.classList.add("animate-jump");
    isFirstLoad = false;
  } else {
    if (jump.classList.contains("animate-jump")) {
      jump.classList.remove("animate-jump");
      jump.classList.add("animate-snooze");
      jump.style.transform = `translate(-115px, -500px)`;
    } else {
      jump.classList.remove("animate-snooze");
      jump.classList.add("animate-jump");
      jump.style.transform = `translate(0px, 0px)`;
    }
  }

  // Check if the Robot is Sleeping, then Switch to Wake Up, and Vice Versa
  if (zzz.classList.contains("snores")) {
    zzz.classList.remove("snores");
    // Hide the "ZZZ" Text and Stop the Snoring Animation
    zzz.style.color = "rgba(0, 0, 0, 0)";
    const snoreElements = zzz.querySelectorAll(".snore");
    snoreElements.forEach((snore) => {
      snore.style.animation = "none";
    });
  } else {
    zzz.classList.add("snores");
    // Show the "ZZZ" Text and Restart the Snoring Animation
    zzz.style.color = "";
    const snoreElements = zzz.querySelectorAll(".snore");
    snoreElements.forEach((snore, index) => {
      snore.style.animation = `snoring 5s linear ${3 + index}s infinite`;
    });
  }

  // Check if the Left Eye is in Sleep Mode, then Switch to Blink, and Vice Versa
  if (leftEye.classList.contains("animate-sleep")) {
    leftEye.classList.remove("animate-sleep");
    leftEye.classList.remove("zzz");
    leftEye.classList.add("animate-blink");
  } else {
    leftEye.classList.remove("animate-blink");
    leftEye.classList.add("animate-sleep", "zzz");
  }

  // Check if the Right Eye is in Sleep Mode, then Switch to Blink, and Vice Versa
  if (rightEye.classList.contains("animate-sleep")) {
    rightEye.classList.remove("animate-sleep");
    leftEye.classList.remove("zzz");
    rightEye.classList.add("animate-blink");
  } else {
    rightEye.classList.remove("animate-blink");
    rightEye.classList.add("animate-sleep", "zzz");
  }

  // Check if the Orb is Off, then Switch to On, and Vice Versa
  if (orb1.classList.contains("off")) {
    orb1.classList.remove("off");
    orb1.classList.add("on");
  } else {
    orb1.classList.remove("on");
    orb1.classList.add("off");
  }

  // Check if the Orb is Off, then Switch to On, and Vice Versa
  if (orb2.classList.contains("off")) {
    orb2.classList.remove("off");
    orb2.classList.add("on");
  } else {
    orb2.classList.remove("on");
    orb2.classList.add("off");
  }
}

document.addEventListener("keydown", function (event) {
  if (event.key === "n") {
    window.location.href = "/trigger/n";
  }
});

var dialogShown = false;

function showDialog() {
  var dialogElement = document.getElementById("dialog");

  var box = setTimeout(function () {
    dialogElement.style.display = "block";
  }, 3000);

  var one = setTimeout(function () {
    dialogElement.querySelector("p").innerText =
      "Hello! My name is Ada, your friendly virtual assistant.";
  }, 0);

  var two = setTimeout(function () {
    var talk1 = document.getElementById("talk1");
    talk1.play();
    dialogElement.querySelector("p").innerText =
      "I'm here to style to today. Shall we begin?";
  }, 6000);

  var three = setTimeout(function () {
    var talk2 = document.getElementById("talk2");
    talk2.play();
    dialogElement.querySelector("p").innerText =
      "Give me a thumbs-up to start!";
  }, 9000);

  dialogShown = true;

  var hideTimeout = setTimeout(function () {
    closeDialog();
  }, 12000); // Change this to Set the Duration of the Last Dialog
}

function closeDialog() {
  document.getElementById("dialog").style.display = "none";
}

function playEnterSound() {
  document.getElementById("jump").play();
}
