let duplicateButton = document.getElementById("duplicate-button");
duplicateButton.addEventListener("click", function() {
    let form = document.getElementById("Create");
    let Category = form.querySelector("Categories_select").cloneNode(true);
    let Product = form.querySelector("Product_name").cloneNode(true);
    form.appendChild(Category);
    form.appendChild(Product);
});
