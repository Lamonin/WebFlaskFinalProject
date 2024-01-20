function updateRentPrice() {
    let startDateInput = document.getElementById("rent-date-start");
    let endDateInput = document.getElementById("rent-date-end");
    let carRentPriceElement = document.getElementById("car-rent-price");
    let selectedCarCost = parseFloat(document.getElementById("selected_car_cost").value);

    let startDate = new Date(startDateInput.value);
    let endDate = new Date(endDateInput.value);

    let timeDiff = Math.abs(endDate.getTime() - startDate.getTime());
    let daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));

    endDate.setDate(startDate.getDate() + 1);
    if (startDate >= endDate) {
        endDateInput.value = endDate.toISOString().slice(0, 10);
    }
    endDateInput.min = endDate.toISOString().slice(0, 10);

    carRentPriceElement.textContent = selectedCarCost * daysDiff;
}

(function (window, document, undefined) {

    window.onload = init;

    function init() {
        updateRentPrice();
    }

})(window, document, undefined);