$(document).ready(function() {
  $("#range-slider").val(10000)
  updateCalculator()
  $("#range-slider").on("change", updateCalculator)
  $(".term-selection").on("change", updateCalculator)
})


function updateCalculator() {
  var formData = {
    "amount": $("#range-slider").val(),
    "term": $(".term-selection input:checked").val()
  }

  $.get("/calculate_fee", formData, function(response) {
    $("#fee").html("£ " + response["fee"])
    $("#amount").html("£ " + response["amount"])
  })
}
