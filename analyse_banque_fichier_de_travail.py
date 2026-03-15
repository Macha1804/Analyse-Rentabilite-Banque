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
# === VÉRIFICATION ===
print("\n📊 Nombre de lignes par table :")
print(f"Clients : {con.execute('SELECT COUNT(*) FROM clients').fetchone()[0]}")
print(f"Transactions : {con.execute('SELECT COUNT(*) FROM transactions').fetchone()[0]}")
print(f"Produits : {con.execute('SELECT COUNT(*) FROM produits_souscrits').fetchone()[0]}")
print(f"Nombre de lignes : {con.execute('SELECT COUNT(*) FROM recap_rentabilite').fetchone()[0]}")

# %%
# === EXPLORATION : Aperçu des données ===
print("\n👥 CLIENTS (5 premières lignes) :")
result = con.execute("SELECT * FROM clients LIMIT 5").fetchdf()
print(result)

# %%
# === REQUÊTE 1 : Distribution par emploi ===
print("\n📊 Distribution des clients par emploi :")
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
print("\n💰 Top 10 clients par balance :")
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
print("\n💸 Revenus des transactions (Top 10 clients) :")
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
# Q1 : Profit total de la banque
result = con.execute("""
    SELECT SUM(profit_net) AS profit_total
           FROM recap_rentabilite
""").fetchdf()
print("💰 PROFIT TOTAL :")
print(result)

# %%
# Q2 : Profit moyen par client
result = con.execute("""
    SELECT AVG(profit_net) AS profit_moyen
           FROM recap_rentabilite
""").fetchdf()
print("📊 PROFIT MOYEN :")
print(result)

# %%
# Q3 : Répartition par segment
result = con.execute("""
    SELECT segment_calcule,
           COUNT(*) AS nb_clients,
           ROUND(COUNT(*) * 100.0/ (SELECT COUNT(*) FROM recap_rentabilite),1) AS pourcentage
           FROM recap_rentabilite
           GROUP BY segment_calcule
           ORDER BY nb_clients DESC
""").fetchdf()
print("🎯 SEGMENTS :")
print(result)


# %%
# Q4 : Top 20 Clients
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net desc
           LIMIT 20
""").fetchdf()
print("🎯 TOP 20 Clients :")
print(result)


# %%
# Q5 : Bottom 20 clients
result = con.execute("""
    SELECT client_id,
           ROUND(profit_net, 2) AS profit_net,
           segment_calcule
           FROM recap_rentabilite
           ORDER BY profit_net ASC
           LIMIT 20
""").fetchdf()
print("🎯 BOTTOM 20 CLIENTS :")
print(result)

# %%
# ========================================
# APERÇU DES TABLES
# ========================================

# %%
# TABLE 1 : CLIENTS
print("\n👥 TABLE CLIENTS (5 premières lignes) :")
result = con.execute("SELECT * FROM clients LIMIT 5").fetchdf()
print(result)

# %%
# TABLE 2 : TRANSACTIONS
print("\n💳 TABLE TRANSACTIONS (5 premières lignes) :")
result = con.execute("SELECT * FROM transactions LIMIT 5").fetchdf()
print(result)

# %%
# TABLE 3 : PRODUITS SOUSCRITS
print("\n📦 TABLE PRODUITS_SOUSCRITS (5 premières lignes) :")
result = con.execute("SELECT * FROM produits_souscrits LIMIT 5").fetchdf()
print(result)

# %%
# TABLE 4 : RECAP RENTABILITÉ (calculée)
print("\n💰 TABLE RECAP_RENTABILITE (5 premières lignes) :")
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
print("🎯 20 les plus rentables :")
print(result)
