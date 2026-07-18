from django.db import models


class Product(models.Model):
    """
    Product model.
    Every product has: a name, description, price, image, and stock quantity.
    """
    name = models.CharField(max_length=200, verbose_name="Product name")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(upload_to='products/', verbose_name="Image")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock quantity")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def is_out_of_stock(self):
        """Returns True if the product is out of stock"""
        return self.stock == 0

    def is_low_stock(self):
        """Returns True if stock is low (below 5, but not zero)"""
        return 0 < self.stock < 5
