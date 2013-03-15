# PostgreSQL COPY command to import bulk data file.

COPY transaction
(recipt_lnr, product_lnr, time_lnr, sales_datetime, store_lnr, customer_lnr, product_quantity_weight, gross_sales)
FROM '/home/ubuntu/info296-ng/data/hsl_ba003t_uttrekk_mw201303111.txt'
WITH CSV HEADER DELIMITER AS E'\t';