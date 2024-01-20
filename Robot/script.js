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
    // You can replace " " with the key you want to trigger the animation
    toggleEyeAnimation();
  }
});

function toggleEyeAnimation() {
  const leftEye = document.querySelector(".robot-eye-left");
  const rightEye = document.querySelector(".robot-eye-right");

  // Check if the left eye is in sleep mode, then switch to blink, and vice versa
  if (leftEye.classList.contains("animate-sleep")) {
    leftEye.classList.remove("animate-sleep");
    leftEye.classList.remove("zzz");
    leftEye.classList.add("animate-blink");
  } else {
    leftEye.classList.remove("animate-blink");
    leftEye.classList.add("animate-sleep", "zzz");
  }

  // Check if the right eye is in sleep mode, then switch to blink, and vice versa
  if (rightEye.classList.contains("animate-sleep")) {
    rightEye.classList.remove("animate-sleep");
    leftEye.classList.remove("zzz");
    rightEye.classList.add("animate-blink");
  } else {
    rightEye.classList.remove("animate-blink");
    rightEye.classList.add("animate-sleep", "zzz");
  }
}
