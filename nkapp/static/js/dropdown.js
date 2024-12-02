document.addEventListener("DOMContentLoaded", function () {
    const dropdowns = document.querySelectorAll("select[data-target]");

    dropdowns.forEach(dropdown => {
        const targetGroup = document.getElementById(dropdown.dataset.target);

        // ページ読み込み時にlocalStorageから選択状態を取得
        const savedValue = localStorage.getItem(`dropdown_${dropdown.id}`);
        if (savedValue) {
            dropdown.value = savedValue;
            showField(targetGroup, savedValue);
        } else {
            // 初期状態で全てのフィールドを非表示
            targetGroup.querySelectorAll(".field").forEach(field => {
                field.style.display = "none";
            });
        }

        // ドロップダウンリストの変更イベント
        dropdown.addEventListener("change", function () {
            const selectedValue = dropdown.value;

            // 選択された値をlocalStorageに保存
            localStorage.setItem(`dropdown_${dropdown.id}`, selectedValue);

            // ターゲットグループ内の全フィールドを非表示
            targetGroup.querySelectorAll(".field").forEach(field => {
                field.style.display = "none";
            });

            // 選択された値に応じて対応するフィールドを表示
            showField(targetGroup, selectedValue);
        });
    });

    // 選択に応じたフィールドを表示する関数
    function showField(targetGroup, selectedValue) {
        const selectedField = targetGroup.querySelector(`.field[data-value="${selectedValue}"]`);
        if (selectedField) {
            selectedField.style.display = "block";
        }
    }
});
