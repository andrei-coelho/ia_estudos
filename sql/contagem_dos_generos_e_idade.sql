SELECT 
    genero,
    CASE 
        WHEN TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) <= 35 THEN '35-'
        ELSE '35+'
    END AS faixa_etaria,
    COUNT(*) AS total
FROM clientes
GROUP BY genero, faixa_etaria;