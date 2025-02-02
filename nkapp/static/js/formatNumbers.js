document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".number-cell").forEach(cell => {
        let text = cell.textContent.trim(); // 空白を削除

        if (text === "") {
            // ① 空文字なら何もしない
            return;
        }

        // ② 数値変換（文字を含む場合はエラー回避）
        let num = Number(text.replace(/,/g, "")); // カンマを除去して数値に変換

        if (!isNaN(num)) {
            // ③ 数値なら千桁区切りを適用
            cell.textContent = num.toLocaleString();
        } else {
            // ④ 数字以外（エラー）の場合は空文字にする
            cell.textContent = "";
        }
    });
});

