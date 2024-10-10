SELECT 
    genero,
    CASE 
        WHEN TIMESTAMPDIFF(YEAR, data_nascimento, CURDATE()) <= 35 THEN 'até 35 anos'
        ELSE 'mais de 35 anos'
    END AS faixa_etaria,
    COUNT(*) AS total
FROM clientes
GROUP BY genero, faixa_etaria;