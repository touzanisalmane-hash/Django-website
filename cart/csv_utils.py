"""
File responsible for creating a CSV file for every successful purchase.
"""
import csv
import os
from django.conf import settings


def create_order_csv(order):
    """
    Creates an order_XXX.csv file inside the orders/ folder with the
    order's details.
    """
    orders_dir = os.path.join(settings.BASE_DIR, 'orders')

    # Create the orders folder if it doesn't exist yet
    os.makedirs(orders_dir, exist_ok=True)

    # File name like order_001.csv, order_002.csv, ...
    file_name = f"order_{order.id:03d}.csv"
    file_path = os.path.join(orders_dir, file_name)

    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow([
            'Order ID', 'Username', 'Email',
            'Purchase date and time', 'Product name', 'Quantity',
            'Unit price', 'Line total'
        ])

        # Write one row per product in the order
        for item in order.items.all():
            writer.writerow([
                order.id,
                order.user.username,
                order.user.email,
                order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                item.product.name,
                item.quantity,
                item.price,
                item.get_total(),
            ])

        # Final row with the order's grand total
        writer.writerow([])
        writer.writerow(['Order grand total', '', '', '', '', '', '', order.total_price])

    return file_path
