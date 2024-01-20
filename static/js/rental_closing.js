
(function (window, document, undefined) {

    window.onload = init;

    function init() {
        const damageSelect = document.getElementById('damage-select');
        const newDamageButton = document.querySelector('[name="new_damage"]');

        damageSelect.addEventListener('change', function() {
          newDamageButton.disabled = damageSelect.value === "-1";
        });

        newDamageButton.disabled = damageSelect.value === "-1";
    }

})(window, document, undefined);