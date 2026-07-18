// Simple JavaScript: confirm before removing a product from the cart
document.addEventListener('DOMContentLoaded', function () {
    const removeButtons = document.querySelectorAll('.btn-remove-item');
    removeButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const confirmDelete = confirm('Are you sure you want to remove this product from the cart?');
            if (!confirmDelete) {
                e.preventDefault();
            }
        });
    });
});
