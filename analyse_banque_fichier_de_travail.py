# %%
"""
PROJET 1 - ANALYSE DE RENTABILITÉ CLIENT BANCAIRE
Auteur : Renée Michèle
Date : Mars 2026

Ce script analyse la rentabilité d'un portefeuille de 1000 clients bancaires.
Objectif : Segmenter les clients et identifier les leviers d'optimisation.
"""

# %%
# === IMPORTS ===
import duckdb
import pandas as pd
import numpy as np


# %%
# === CONNEXION DUCKDB ===
con = duckdb.connect(':memory:')  # Base de données en mémoire
print("Connexion DuckDB créée")

# %%
# === CHARGEMENT DES DONNÉES ===

# Table clients
con.execute("""
    CREATE TABLE clients AS
    SELECT * FROM read_csv_auto('data/clients.csv')
""")
print("Table clients chargée")

# Table transactions
con.execute("""
    CREATE TABLE transactions AS
    SELECT * FROM read_csv_auto('data/transactions.csv')
""")
print("Table transactions chargée")

# Table produits
con.execute("""
    CREATE TABLE produits_souscrits AS
    SELECT * FROM read_csv_auto('data/produits_souscrits.csv')
""")
print("Table produits_souscrits chargée")

# Table recap_rentabilite
# %%
# === CHARGER LA TABLE RECAP_RENTABILITE ===
con.execute("""
    CREATE TABLE recap_rentabilite AS
    SELECT * FROM read_csv_auto('data/recap_rentabilite.csv')
""")
print("Table recap_rentabilite chargée")


# %%
# === VÉRIFICATION ===
print("\n Nombre de lignes par table :")
print(f"Clients : {con.execute('SELECT COUNT(*) FROM clients').fetchone()[0]}")
print(f"Transactions : {con.execute('SELECT COUNT(*) FROM transactions').fetchone()[0]}")
print(f"Produits : {con.execute('SELECT COUNT(*) FROM produits_souscrits').fetchone()[0]}")
print(f"Nombre de lignes : {con.execute('SELECT COUNT(*) FROM recap_rentabilite').fetchone()[0]}")

# %%
# === EXPLORATION : Aperçu des données ===
print("\n CLIENTS (5 premières lignes) :")
result = con.execute("SELECT * FROM clients LIMIT 5").fetchdf()
print(result)

# %%
# === REQUÊTE 1 : Distribution par emploi ===
print("\n Distribution des clients par emploi :")
result = con.execute("""
    SELECT
        emploi,
        COUNT(*) as nb_clients,
        ROUND(AVG(balance_moyenne), 2) as balance_moyenne
    FROM clients
    GROUP BY emploi
    ORDER BY nb_clients DESC
""").fetchdf()
print(result)

# %%
# === REQUÊTE 2 : Top 10 clients par balance ===
print("\n Top 10 clients par balance :")
result = con.execute("""
    SELECT
        client_id,
        nom_complet,
        emploi,
        balance_moyenne
    FROM clients
    ORDER BY balance_moyenne DESC
    LIMIT 10
""").fetchdf()
print(result)

# %%
# === REQUÊTE 3 : Revenus transactions par client ===
print("\n Revenus des transactions (Top 10 clients) :")
result = con.execute("""
    SELECT
        client_id,
        COUNT(*) as nb_transactions,
        ROUND(SUM(frais_generes), 2) as total_frais
    FROM transactions
    GROUP BY client_id
    ORDER BY total_frais DESC
    LIMIT 10
""").fetchdf()
print(result)

# %%
# === À TOI DE JOUER ! ===
# Écris tes propres requêtes ici

# %%
# ========================================
# THÈME 1 : RENTABILITÉ GLOBALE
# ========================================

# %%
# Profit total de la banque
result = con.execute("""
    SELECT SUM(profit_net) AS profit_total
           FROM recap_rentabilite
""").fetchdf()
print(" PROFIT TOTAL :")
print(result)

# %%
# Profit moyen par client
result = con.execute("""
    SELECT AVG(profit_net) AS profit_moyen
           FROM recap_rentabilite
""").fetchdf()
print(" PROFIT MOYEN :")
print(result)

# %%
# Répartition par segment
result = con.execute("""
    SELECT segment_calcule,
           COUNT(*) AS nb_clients,
           ROUND(COUNT(*) * 100.0/ (SELECT COUNT(*) FROM recap_rentabilite),1) AS pourcentage
           FROM recap_rentabilite
           GROUP BY segment_calcule
           ORDER BY nb_clients DESC
""").fetchdf()
print("SEGMENTS :")
print(result)


# %%
# Top 20 Clients
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net desc
           LIMIT 20
""").fetchdf()
print("TOP 20 Clients :")
print(result)


# %%
# Bottom 20 clients
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net ASC
           LIMIT 20
""").fetchdf()
print("BOTTOM 20 CLIENTS :")
print(result)

# %%
# ========================================
# APERÇU DES TABLES
# ========================================

# %%
# TABLE 1 : CLIENTS
print("\n TABLE CLIENTS (5 premières lignes) :")
result = con.execute("SELECT * FROM clients LIMIT 5").fetchdf()
print(result)

# %%
# TABLE 2 : TRANSACTIONS
print("\n TABLE TRANSACTIONS (5 premières lignes) :")
result = con.execute("SELECT * FROM transactions LIMIT 5").fetchdf()
print(result)

# %%
# TABLE 3 : PRODUITS SOUSCRITS
print("\n TABLE PRODUITS_SOUSCRITS (5 premières lignes) :")
result = con.execute("SELECT * FROM produits_souscrits LIMIT 5").fetchdf()
print(result)

# %%
# TABLE 4 : RECAP RENTABILITÉ (calculée)
print("\n TABLE RECAP_RENTABILITE (5 premières lignes) :")
result = con.execute("SELECT * FROM recap_rentabilite LIMIT 5").fetchdf()
print(result)

# %%
# Q6 : 20% les plus rentables
result = con.execute("""
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
             ((top_200.profit_top / total.profit_total)*100) AS pourcentage
             FROM top_200, total
""").fetchdf()
print("20 les plus rentables :")
print(result)

# Q7 : Produits les plus rentables
result = con.execute(""" SELECT produit,
       SUM(profit_annuel) AS sum_profit,
       COUNT(client_id) AS nombre_de_client,
       AVG(profit_annuel) AS profit_moyen_par_produit
FROM produits_souscrits
GROUP BY produit
ORDER BY sum_profit DESC
""").fetchdf()
print("les plus rentables :")
print(result)

# Nombre de clients par produit
result = con.execute("""SELECT produit,
       COUNT(client_id) AS nombre_de_client
FROM produits_souscrits
GROUP BY produit
ORDER BY nombre_de_client DESC
""").fetchdf()
print("Nombre de clients par produit :")
print(result)

#  Produits des clients VIP
result = con.execute("""SELECT p.produit,
       COUNT(p.client_id) AS nombre_de_client
FROM produits_souscrits p
INNER JOIN recap_rentabilite r ON p.client_id = r.client_id
WHERE r.segment_calcule = 'VIP'
GROUP BY p.produit
ORDER BY nombre_de_client DESC
""").fetchdf()
print("Produits des clients VIP :")
print(result)

# Rentabilité par type d'emploi
result = con.execute("""SELECT c.emploi,
       SUM(r.profit_net) AS sum_profit,
       AVG(r.profit_net) AS avg_profit,
       COUNT(c.client_id) AS nombre_de_clients
FROM clients c
INNER JOIN recap_rentabilite r ON c.client_id = r.client_id
GROUP BY c.emploi
ORDER BY avg_profit DESC
""").fetchdf()
print("Rentabilité par type d'emploi :")
print(result)

#  Part transactions vs produits dans le revenu
result = con.execute("""SELECT SUM(revenus_transactions) AS revenus_transactions_total,
       SUM(revenus_annuels) AS revenus_produits_total,
       ROUND((SUM(revenus_transactions)/(SUM(revenus_transactions)+SUM(revenus_annuels))*100),1) AS pct_revenus_transactions,
       ROUND((SUM(revenus_annuels)/(SUM(revenus_transactions)+SUM(revenus_annuels))*100),1) AS pct_revenus_produits
FROM recap_rentabilite
""").fetchdf()
print("Part transactions vs produits dans le revenu :")
print(result)


# Part de Cadre avec le crédit immobilier
result = con.execute("""WITH total_cadre AS (
    SELECT COUNT(client_id) AS nombre_total_cadre
    FROM clients
    WHERE emploi = 'Cadre'
),
cadre_immobilier AS (
    SELECT COUNT(c.client_id) AS nombre_credit_immobilier
    FROM clients c
    INNER JOIN produits_souscrits p ON c.client_id = p.client_id
    WHERE c.emploi = 'Cadre'
    AND p.produit = 'Crédit Immobilier'
)
SELECT
    ca.nombre_credit_immobilier,
    tc.nombre_total_cadre,
    ROUND((ca.nombre_credit_immobilier / tc.nombre_total_cadre) * 100, 1) AS pourcentage
FROM cadre_immobilier ca, total_cadre tc
""").fetchdf()
print("Part de Cadre avec le crédit immobilier:")
print(result)


#Profit moyen par client
result = con.execute("""SELECT segment_calcule,
                        AVG(profit_net) AS profit_moyen
                        FROM recap_rentabilite
                        GROUP BY segment_calcule
                        ORDER BY profit_moyen DESC
""").fetchdf()
print("Profit moyen par client:")
print(result)

#Profit moyen par emploi
result = con.execute("""SELECT c.emploi,
       AVG(r.profit_net) AS profit_moyen,
       COUNT(c.client_id) AS nombre_clients,
       SUM(r.profit_net) AS profit_total
FROM clients c
INNER JOIN recap_rentabilite r ON c.client_id = r.client_id
GROUP BY c.emploi
ORDER BY profit_moyen DESC
""").fetchdf()
print("Profit moyen par emploi:")
print(result)

#frais générés
result = con.execute("""SELECT type_transaction,
                                SUM(frais_generes) AS somme_de_frais
                        FROM transactions
                        GROUP BY type_transaction
                        ORDER BY SUM(frais_generes) DESC
""").fetchdf()
print("Frais générés:")
print(result)

# Nombre de transactions par client et par segment
result = con.execute("""WITH nombre_de_transactions AS (SELECT COUNT(transaction_id) AS nbr_transactions,
                                                        client_id FROM transactions GROUP BY client_id)
                                                        SELECT AVG(nbr_transactions) AS moyenne_transactions,
                                                        rp.segment_calcule
                                                        FROM nombre_de_transactions nt
                                                        INNER JOIN recap_rentabilite rp ON nt.client_id = rp.client_id
                                                        GROUP BY rp.segment_calcule ORDER BY moyenne_transactions DESC
""").fetchdf()
print("Nombre de transactions par client et par segment:")
print(result)
