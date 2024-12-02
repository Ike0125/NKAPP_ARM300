document.addEventListener("DOMContentLoaded", function () { 
    const parents = document.querySelectorAll(".parent");
    const dropdown = document.getElementById("dropdown");

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
        parent.addEventListener("click", () => {
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

    // ドロップダウンリストの選択に応じてTreeviewを開閉
    dropdown.addEventListener("change", function() {
        const selectedCategory = dropdown.value;

        parents.forEach((parent, index) => {
            const category = parent.getAttribute("data-category");
            const child = parent.nextElementSibling;

            if (category === selectedCategory) {
                parent.classList.add("caret-down");
                child.style.display = "block";
                localStorage.setItem(`tree_${index}`, true);
            } else {
                parent.classList.remove("caret-down");
                child.style.display = "none";
                localStorage.setItem(`tree_${index}`, false);
            }
        });
    });
});
