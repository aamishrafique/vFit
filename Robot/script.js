document.getElementsByTagName("h1")[0].style.fontSize = "6vw";

document.addEventListener("DOMContentLoaded", function () {
  function randomDirection() {
    const directions = ["left", "right", "center"];
    return directions[Math.floor(Math.random() * directions.length)];
  }

  function setEyeDirection() {
    const eyeLeft = document.querySelector(".robot-eye-left");
    const eyeRight = document.querySelector(".robot-eye-right");

    const directionLeft = randomDirection();
    const directionRight = randomDirection();

    eyeLeft.style.transformOrigin = `${directionLeft} center`;
    eyeRight.style.transformOrigin = `${directionRight} center`;
  }

  setInterval(setEyeDirection, 4000);
});
