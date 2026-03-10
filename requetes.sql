-- ========================================
-- ANALYSE DE RENTABILITÉ CLIENT BANCAIRE
-- 6 Requêtes SQL Essentielles
-- ========================================

-- Q1 : Profit total de la banque
SELECT SUM(profit_net) AS profit_total
FROM recap_rentabilite;

-- Q2 : Profit moyen par client
SELECT AVG(profit_net) AS profit_moyen
FROM recap_rentabilite;

-- Q3 : Répartition des clients par segment
SELECT
    segment_calcule,
    COUNT(*) AS nb_clients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM recap_rentabilite), 1) AS pourcentage
FROM recap_rentabilite
GROUP BY segment_calcule
ORDER BY nb_clients DESC;

-- Q4 : Top 20 clients les plus rentables
SELECT
    nom_complet,
    emploi,
    ROUND(profit_net, 2) AS profit_net,
    segment_calcule
FROM recap_rentabilite
ORDER BY profit_net DESC
LIMIT 20;

-- Q5 : Bottom 20 clients les moins rentables
SELECT
    nom_complet,
    emploi,
    ROUND(profit_net, 2) AS profit_net,
    segment_calcule
FROM recap_rentabilite
ORDER BY profit_net ASC
LIMIT 20;

-- Q6 : Principe de Pareto - Les 20% clients les plus rentables
WITH top_200 AS (
    SELECT SUM(profit_net) AS profit_top
    FROM (
        SELECT profit_net
        FROM recap_rentabilite
        ORDER BY profit_net DESC
        LIMIT 200
    ) AS top_clients
),
total AS (
    SELECT SUM(profit_net) AS profit_total
    FROM recap_rentabilite
)
SELECT
    top_200.profit_top,
    total.profit_total,
    ROUND((top_200.profit_top / total.profit_total) * 100, 1) AS pourcentage
FROM top_200, total;
