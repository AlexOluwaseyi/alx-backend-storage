-- Update table based on value in anothe table

UPDATE items
JOIN orders ON items.name = orders.item_name
SET items.quantity = items.quantity - orders.number
