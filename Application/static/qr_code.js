document.addEventListener("DOMContentLoaded", function () {
  // Function to Play the Enter Sound
  function playEnterSound() {
    document.getElementById("talk1").play();
  }

  // Function to Show the Dialog
  function showDialog() {
    var dialogElement = document.getElementById("dialog");

    var one = setTimeout(function () {
      dialogElement.querySelector("p").innerText =
        "\nScan the QR Code to download\nyour result.";
    }, 0);

    dialogElement.style.display = "block";

    // var hideTimeout = setTimeout(function () {
    //   closeDialog();
    // }, 30000);
  }

  // Function to Close the Dialog
  function closeDialog() {
    document.getElementById("dialog").style.display = "none";
  }

  playEnterSound();
  showDialog();
});
