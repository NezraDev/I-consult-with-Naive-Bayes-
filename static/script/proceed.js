document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(".symptom-checkbox");
  const proceedBtn = document.getElementById("proceed-button");

  function updateProceedState() {
    const anyChecked = Array.from(checkboxes).some((cb) => cb.checked);
    proceedBtn.disabled = !anyChecked;
    proceedBtn.classList.toggle("opacity-50", !anyChecked);
    proceedBtn.classList.toggle("cursor-not-allowed", !anyChecked);
  }

  updateProceedState();

  checkboxes.forEach((cb) => cb.addEventListener("change", updateProceedState));
});
