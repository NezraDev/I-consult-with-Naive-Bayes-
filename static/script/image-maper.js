$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const selectedPartsParam = urlParams.get("part");
  window.selectedBodyParts = [];

  $("img").mapster({
    fillColor: "643dff",
    strokeColor: "643dff",
    strokeOpacity: 0.8,
    fillOpacity: 0.4,
    strokeWidth: 2,
    stroke: true,
    singleSelect: false, // Allow multiple selection
    isSelectable: false, // Allow toggling
    mapKey: "name",

    onClick: function (e) {
      const key = e.key;
      const index = window.selectedBodyParts.indexOf(key);

      if (index > -1) {
        // Deselect part
        window.selectedBodyParts.splice(index, 1);
        $("img").mapster("set", false, key);
      } else {
        // Select part
        window.selectedBodyParts.push(key);
        $("img").mapster("set", true, key);
      }

      return true;
    },
  });

  // Handle selections from URL
  if (selectedPartsParam) {
    window.selectedBodyParts = selectedPartsParam.split(",");
    window.selectedBodyParts.forEach((part) => {
      $("img").mapster("set", true, part);
    });
  }

  $("#proceed-button").click(function (e) {
    if (!window.selectedBodyParts || window.selectedBodyParts.length === 0) {
      alert("Please select at least one body part.");
      e.preventDefault();
      return false;
    } else {
      const selectedPartsString = window.selectedBodyParts.join(",");
      const baseUrl = $(this).closest("a").attr("href").split("?")[0];
      $(this)
        .closest("a")
        .attr("href", `${baseUrl}?part=${selectedPartsString}`);
      return true;
    }
  });
});
