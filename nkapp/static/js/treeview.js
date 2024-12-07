// Tree Viewの状態を保存・復元する関数
document.addEventListener("DOMContentLoaded", function () {
    const parents = document.querySelectorAll(".parent");

    parents.forEach((parent, index) => {
        const isOpen = localStorage.getItem(`tree_${index}`) === "true";
        const child = parent.nextElementSibling;

        // マークを初期状態に設定
        if (isOpen) {
            parent.classList.add("caret-down");
            child.style.display = "block";
        } else {
            parent.classList.remove("caret-down");
            child.style.display = "none";
        }

        // クリックイベントで開閉とマーク切り替え
        parent.addEventListener("click", (event) => {
            // チェックボックスがクリックされた場合は処理しない
            if (event.target.tagName === "INPUT" && event.target.type === "checkbox") {
                return;
            }

            const currentlyOpen = child.style.display === "block";
            child.style.display = currentlyOpen ? "none" : "block";

            // マークの切り替え
            if (currentlyOpen) {
                parent.classList.remove("caret-down");
            } else {
                parent.classList.add("caret-down");
            }

            // 状態をlocalStorageに保存
            localStorage.setItem(`tree_${index}`, !currentlyOpen);
        });
    });
});
