-- SQL script that lists all bands with Glam rock as
-- their main style, ranked by their longevity

SELECT band_name AS 'band_name', 
COALESCE(split - formed, 2022 - formed) AS 'lifespan'
-- COALESCE(2022 - formed, split - formed) AS 'lifespan'
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY 'lifespan' DESC;
