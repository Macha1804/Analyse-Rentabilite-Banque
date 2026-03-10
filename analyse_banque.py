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


# %%
# === CONNEXION DUCKDB ===
con = duckdb.connect(':memory:')  # Base de données en mémoire
print("Connexion DuckDB créée")

# %%
# === CHARGEMENT DES DONNÉES ===

# Table clients
con.execute("""
    CREATE TABLE clients AS
    SELECT * FROM read_csv_auto('clients.csv')
""")
print("Table clients chargée")

# Table transactions
con.execute("""
    CREATE TABLE transactions AS
    SELECT * FROM read_csv_auto('transactions.csv')
""")
print("Table transactions chargée")

# Table produits
con.execute("""
    CREATE TABLE produits_souscrits AS
    SELECT * FROM read_csv_auto('produits_souscrits.csv')
""")
print("Table produits_souscrits chargée")

# Table recap_rentabilite
# %%
# === CHARGER LA TABLE RECAP_RENTABILITE ===
con.execute("""
    CREATE TABLE recap_rentabilite AS
    SELECT * FROM read_csv_auto('recap_rentabilite.csv')
""")
print("Table recap_rentabilite chargée")


# %%
# ========================================
# THÈME 1 : ANALYSES SQL
# ========================================

# %%
print("\n Q1 : PROFIT TOTAL")
result = con.execute("""
    SELECT SUM(profit_net) AS profit_total
           FROM recap_rentabilite
""").fetchdf()
print(result)

# %%
print("\n Q2 : PROFIT MOYEN")
result = con.execute("""
    SELECT AVG(profit_net) AS profit_moyen
           FROM recap_rentabilite
""").fetchdf()
print(result)

# %%
print("\n Q3 : REPARTITION PAR SEGMENT")
result = con.execute("""
    SELECT segment_calcule,
           COUNT(*) AS nb_clients,
           ROUND(COUNT(*) * 100.0/ (SELECT COUNT(*) FROM recap_rentabilite),1) AS pourcentage
           FROM recap_rentabilite
           GROUP BY segment_calcule
           ORDER BY nb_clients DESC
""").fetchdf()
print(result)


# %%
print("\n Q4 : TOP 20 CLIENTS")
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net desc
           LIMIT 20
""").fetchdf()
print(result)


# %%
print("\n Q5 : BOTTOM 20 CLIENTS")
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net ASC
           LIMIT 20
""").fetchdf()
print(result)

# %%
print("\n Q6 : PRINCIPE DE PARETO")
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
print(result)

print("\n Analyse terminée !")
