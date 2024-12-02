document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("dropdown101");

    // 各入力フィールドの要素を取得
    const gap101 = document.getElementById("gap101").parentNode;
    const param101 = document.getElementById("param101").parentNode;
    const param102 = document.getElementById("param102").parentNode;

    // 初期状態で全てを非表示（位置は保持）
    gap101.style.visibility = "hidden";
    gap101.style.height = "0";
    param101.style.visibility = "hidden";
    param101.style.height = "0";
    param102.style.visibility = "hidden";
    param102.style.height = "0";

    // ドロップダウンリストの変更イベント
    dropdown.addEventListener("change", function () {
        const selectedValue = dropdown.value;

        // 全て非表示（位置は保持）
        gap101.style.visibility = "hidden";
        gap101.style.height = "0";
        param101.style.visibility = "hidden";
        param101.style.height = "0";
        param102.style.visibility = "hidden";
        param102.style.height = "0";

        // 選択された値に応じて表示（位置を固定解除）
        if (selectedValue === "0200") {
            gap101.style.visibility = "visible";
            gap101.style.height = ""; // 元の高さに戻す
        } else if (selectedValue === "0201") {
            param101.style.visibility = "visible";
            param101.style.height = ""; // 元の高さに戻す
        } else if (selectedValue === "0202") {
            param102.style.visibility = "visible";
            param102.style.height = ""; // 元の高さに戻す
        }
    });
});
