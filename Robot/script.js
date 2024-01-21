// document.getElementsByTagName("h1")[0].style.fontSize = "6vw";

// document.addEventListener("DOMContentLoaded", function () {
//   function randomDirection() {
//     const directions = ["left", "right", "center"];
//     return directions[Math.floor(Math.random() * directions.length)];
//   }

//   function setEyeDirection() {
//     const eyeLeft = document.querySelector(".robot-eye-left");
//     const eyeRight = document.querySelector(".robot-eye-right");

//     const directionLeft = randomDirection();
//     const directionRight = randomDirection();

//     eyeLeft.style.transformOrigin = `${directionLeft} center`;
//     eyeRight.style.transformOrigin = `${directionRight} center`;
//   }

//   setInterval(setEyeDirection, 4000);
// });

document.addEventListener("keydown", function (event) {
  if (event.key === " ") {
    sleepAwakeState();
  }
});

function sleepAwakeState() {
  const leftEye = document.querySelector(".robot-eye-left");
  const rightEye = document.querySelector(".robot-eye-right");
  const innerBody = document.querySelector(".inner");
  const zzz = document.querySelector(".wake-up");
  const orb1 = document.querySelector(".orb1");
  const orb2 = document.querySelector(".orb2");
  const jump = document.querySelector(".robot-container");

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

  // Check if the Robot is Sleeping, then Stay, else, Jump, and Vice Versa
  if (jump.classList.contains("animate-stay")) {
    jump.classList.remove("animate-stay");
    jump.classList.add("animate-jump");
  } else {
    jump.classList.remove("animate-jump");
    jump.classList.add("animate-stay");
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
