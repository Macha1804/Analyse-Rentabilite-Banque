-- ========================================
-- ANALYSE DE RENTABILITÉ CLIENT BANCAIRE
-- 6 Requêtes SQL Essentielles
-- ========================================

-- Profit total de la banque
SELECT SUM(profit_net) AS profit_total
FROM recap_rentabilite;

-- Profit moyen par client
SELECT AVG(profit_net) AS profit_moyen
FROM recap_rentabilite;

-- Répartition des clients par segment
SELECT
    segment_calcule,
    COUNT(*) AS nb_clients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM recap_rentabilite), 1) AS pourcentage
FROM recap_rentabilite
GROUP BY segment_calcule
ORDER BY nb_clients DESC;

-- Top 20 clients les plus rentables
SELECT
    nom_complet,
    emploi,
    ROUND(profit_net, 2) AS profit_net,
    segment_calcule
FROM recap_rentabilite
ORDER BY profit_net DESC
LIMIT 20;

-- Bottom 20 clients les moins rentables
SELECT
    nom_complet,
    emploi,
    ROUND(profit_net, 2) AS profit_net,
    segment_calcule
FROM recap_rentabilite
ORDER BY profit_net ASC
LIMIT 20;

-- Principe de Pareto - Les 20% clients les plus rentables
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

-- Produits les plus rentables
SELECT produit,
       SUM(profit_annuel) AS sum_profit,
       COUNT(client_id) AS nombre_de_client,
       AVG(profit_annuel) AS profit_moyen_par_produit
FROM produits_souscrits
GROUP BY produit
ORDER BY sum_profit DESC;

-- Nombre de clients par produit
SELECT produit,
       COUNT(client_id) AS nombre_de_client
FROM produits_souscrits
GROUP BY produit
ORDER BY nombre_de_client DESC;

-- Produits des clients VIP
SELECT p.produit,
       COUNT(p.client_id) AS nombre_de_client
FROM produits_souscrits p
INNER JOIN recap_rentabilite r ON p.client_id = r.client_id
WHERE r.segment_calcule = 'VIP'
GROUP BY p.produit
ORDER BY nombre_de_client DESC;

-- Rentabilité par type d'emploi
SELECT c.emploi,
       SUM(r.profit_net) AS sum_profit,
       AVG(r.profit_net) AS avg_profit,
       COUNT(c.client_id) AS nombre_de_clients
FROM clients c
INNER JOIN recap_rentabilite r ON c.client_id = r.client_id
GROUP BY c.emploi
ORDER BY avg_profit DESC;

-- Part transactions vs produits dans le revenu
SELECT SUM(revenus_transactions) AS revenus_transactions_total,
       SUM(revenus_annuels) AS revenus_produits_total,
       ROUND((SUM(revenus_transactions)/(SUM(revenus_transactions)+SUM(revenus_annuels))*100),1) AS pct_revenus_transactions,
       ROUND((SUM(revenus_annuels)/(SUM(revenus_transactions)+SUM(revenus_annuels))*100),1) AS pct_revenus_produits
FROM recap_rentabilite;
