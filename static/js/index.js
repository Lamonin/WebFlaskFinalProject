function checkBoxAllSelect(select_all_id, checkbox_id) {
    function checkAllModels() {
        const selectAllCheckbox = document.getElementById(select_all_id);
        const modelCheckboxes = Array.from(document.getElementsByName(checkbox_id));

        if (selectAllCheckbox.checked) {
            modelCheckboxes.forEach(checkbox => checkbox.checked = true);
        } else {
            modelCheckboxes.forEach(checkbox => checkbox.checked = false);
        }
    }

    function handleModelCheckboxChange() {
        const selectAllCheckbox = document.getElementById(select_all_id);
        const modelCheckboxes = Array.from(document.getElementsByName(checkbox_id));
        const checkedCount = modelCheckboxes.filter(checkbox => checkbox.checked).length;

        selectAllCheckbox.checked = checkedCount === modelCheckboxes.length;
    }

    document.getElementById(select_all_id).addEventListener('change', checkAllModels);
    document.getElementsByName(checkbox_id).forEach(checkbox => checkbox.addEventListener('change', handleModelCheckboxChange));
}

function twoFields(first_field_id, second_field_id) {
    const firstField = document.getElementById(first_field_id);
    const secondField = document.getElementById(second_field_id);

    firstField.addEventListener('change', function () {
        if (parseInt(firstField.value) > parseInt(secondField.value)) {
            let temp = firstField.value;
            firstField.value = secondField.value;
            secondField.value = temp;
        }
    });

    secondField.addEventListener('change', function () {
        if (parseInt(secondField.value) < parseInt(firstField.value)) {
            let temp = secondField.value;
            secondField.value = firstField.value;
            firstField.value = temp;
        }
    });
}

(function (window, document, undefined) {

    window.onload = init;

    function init() {
        checkBoxAllSelect("select_all_model", "car-brand[]");
        checkBoxAllSelect("select_all_color", "car-color[]");
        twoFields("cost-min", "cost-max");
        twoFields("year-min", "year-max");
    }

})(window, document, undefined);