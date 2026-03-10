"""
PROJET 1 - GÉNÉRATION DE DONNÉES BANCAIRES RÉALISTES
Analyse de Rentabilité Client

Ce script génère 3 tables de données bancaires fictives mais réalistes :
1. clients.csv - Informations clients avec coûts d'acquisition
2. transactions.csv - Transactions bancaires avec frais générés
3. produits_souscrits.csv - Produits bancaires par client avec revenus/coûts

Auteur : Renée Michèle
Date : 28 Février 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration pour la reproductibilité
np.random.seed(42)
random.seed(42)

# ============================================================================
# PARTIE 1 : GÉNÉRATION DE LA TABLE CLIENTS
# ============================================================================

print("📊 Génération de la table CLIENTS...")

# Paramètres
N_CLIENTS = 1000

# Générer les IDs clients
client_ids = [f"CLI_{str(i).zfill(4)}" for i in range(1, N_CLIENTS + 1)]

# Générer les noms fictifs
prenoms = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Luc', 'Julie', 'Thomas', 'Emma', 
           'Nicolas', 'Camille', 'Alexandre', 'Laura', 'François', 'Alice', 'David']
noms = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 
        'Durand', 'Leroy', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel']

noms_complets = [f"{random.choice(prenoms)} {random.choice(noms)}" for _ in range(N_CLIENTS)]

# Générer les âges (distribution réaliste)
# Plus de clients entre 30-55 ans (segment actif)
age_probs = []
for age in range(18, 75):
    if age < 25:
        age_probs.append(0.01)
    elif 25 <= age < 35:
        age_probs.append(0.03)
    elif 35 <= age < 55:
        age_probs.append(0.04)
    else:
        age_probs.append(0.02)

# Normaliser pour que la somme = 1
age_probs = np.array(age_probs)
age_probs = age_probs / age_probs.sum()

ages = np.random.choice(range(18, 75), N_CLIENTS, p=age_probs)

# Générer les types d'emploi
emplois = ['Cadre', 'Employé', 'Profession libérale', 'Retraité', 'Étudiant', 
           'Artisan/Commerçant', 'Fonctionnaire', 'Sans emploi']
emplois_weights = [0.20, 0.30, 0.10, 0.15, 0.05, 0.10, 0.08, 0.02]
emplois_clients = np.random.choice(emplois, N_CLIENTS, p=emplois_weights)

# Générer les dates d'acquisition (clients sur les 5 dernières années)
date_debut = datetime(2020, 1, 1)
date_fin = datetime(2025, 12, 31)
dates_acquisition = [
    date_debut + timedelta(days=random.randint(0, (date_fin - date_debut).days))
    for _ in range(N_CLIENTS)
]

# Ancienneté en mois
anciennete_mois = [
    (datetime(2026, 2, 28) - date).days // 30 
    for date in dates_acquisition
]

# Coût d'acquisition (varie selon le canal et l'époque)
# Plus cher pour les clients récents (marketing digital)
couts_acquisition = [
    np.random.uniform(150, 400) if anc < 12 else
    np.random.uniform(100, 300) if anc < 36 else
    np.random.uniform(80, 200)
    for anc in anciennete_mois
]

# Segment initial (sera recalculé après analyse)
segments_initiaux = ['Standard'] * N_CLIENTS

# Balance moyenne du compte (corrélée avec emploi et âge)
def generer_balance(emploi, age):
    if emploi == 'Cadre':
        return np.random.uniform(5000, 50000)
    elif emploi == 'Profession libérale':
        return np.random.uniform(10000, 80000)
    elif emploi == 'Retraité':
        return np.random.uniform(8000, 40000)
    elif emploi == 'Employé':
        return np.random.uniform(2000, 15000)
    elif emploi == 'Étudiant':
        return np.random.uniform(500, 5000)
    elif emploi == 'Artisan/Commerçant':
        return np.random.uniform(3000, 25000)
    elif emploi == 'Fonctionnaire':
        return np.random.uniform(4000, 20000)
    else:
        return np.random.uniform(1000, 8000)

balances = [generer_balance(emp, age) for emp, age in zip(emplois_clients, ages)]

# Créer le DataFrame clients
df_clients = pd.DataFrame({
    'client_id': client_ids,
    'nom_complet': noms_complets,
    'age': ages,
    'emploi': emplois_clients,
    'balance_moyenne': np.round(balances, 2),
    'date_acquisition': [d.strftime('%Y-%m-%d') for d in dates_acquisition],
    'anciennete_mois': anciennete_mois,
    'cout_acquisition': np.round(couts_acquisition, 2),
    'segment': segments_initiaux
})

print(f"✅ {len(df_clients)} clients générés")
print(f"   Âge moyen : {df_clients['age'].mean():.1f} ans")
print(f"   Balance moyenne : {df_clients['balance_moyenne'].mean():.2f} €")

# ============================================================================
# PARTIE 2 : GÉNÉRATION DE LA TABLE TRANSACTIONS
# ============================================================================

print("\n📊 Génération de la table TRANSACTIONS...")

# Générer environ 5 transactions par client (entre 2 et 10)
transactions = []
transaction_id = 1

for idx, client_id in enumerate(client_ids):
    # Nombre de transactions (clients actifs ont plus de transactions)
    balance = balances[idx]
    n_trans = np.random.randint(2, 12) if balance > 10000 else np.random.randint(1, 6)
    
    client_date_acquisition = dates_acquisition[idx]
    
    for _ in range(n_trans):
        # Date de transaction (après acquisition)
        jours_depuis_acquisition = (datetime(2026, 2, 28) - client_date_acquisition).days
        date_trans = client_date_acquisition + timedelta(days=random.randint(0, jours_depuis_acquisition))
        
        # Type de transaction
        type_trans = random.choice([
            'Virement', 'Prélèvement', 'Retrait DAB', 'Paiement carte', 
            'Dépôt', 'Virement reçu', 'Chèque'
        ])
        
        # Montant (varie selon le type)
        if type_trans in ['Virement', 'Virement reçu']:
            montant = np.random.uniform(100, 5000)
        elif type_trans == 'Paiement carte':
            montant = np.random.uniform(10, 500)
        elif type_trans == 'Retrait DAB':
            montant = np.random.uniform(20, 300)
        elif type_trans == 'Dépôt':
            montant = np.random.uniform(50, 2000)
        elif type_trans == 'Chèque':
            montant = np.random.uniform(100, 1000)
        else:
            montant = np.random.uniform(50, 1000)
        
        # Frais générés pour la banque
        if type_trans == 'Retrait DAB':
            frais = 1.5  # Frais fixe DAB
        elif type_trans == 'Paiement carte':
            frais = montant * 0.002  # 0.2% commission
        elif type_trans == 'Virement':
            frais = 0.5 if montant < 1000 else 1.0
        elif type_trans == 'Chèque':
            frais = 0.3
        else:
            frais = 0.0
        
        transactions.append({
            'transaction_id': f"TRX_{str(transaction_id).zfill(6)}",
            'client_id': client_id,
            'date_transaction': date_trans.strftime('%Y-%m-%d'),
            'type_transaction': type_trans,
            'montant': round(montant, 2),
            'frais_generes': round(frais, 2)
        })
        transaction_id += 1

df_transactions = pd.DataFrame(transactions)

print(f"✅ {len(df_transactions)} transactions générées")
print(f"   Moyenne par client : {len(df_transactions)/N_CLIENTS:.1f}")
print(f"   Frais moyens par transaction : {df_transactions['frais_generes'].mean():.2f} €")

# ============================================================================
# PARTIE 3 : GÉNÉRATION DE LA TABLE PRODUITS SOUSCRITS
# ============================================================================

print("\n📊 Génération de la table PRODUITS SOUSCRITS...")

produits_souscrits = []

# Définir les produits bancaires disponibles
produits_bancaires = {
    'Compte Courant': {
        'revenus_annuels': lambda: np.random.uniform(30, 60),  # Frais de tenue de compte
        'cout_gestion': lambda: np.random.uniform(15, 25),
        'probabilite': 1.0  # Tout le monde a un compte courant
    },
    'Carte Bancaire Standard': {
        'revenus_annuels': lambda: 45,  # Frais carte annuels
        'cout_gestion': lambda: 10,
        'probabilite': 0.85
    },
    'Carte Bancaire Premium': {
        'revenus_annuels': lambda: 120,
        'cout_gestion': lambda: 20,
        'probabilite': 0.15  # Seulement clients aisés
    },
    'Compte Épargne': {
        'revenus_annuels': lambda: np.random.uniform(50, 150),  # Intérêts générés
        'cout_gestion': lambda: np.random.uniform(20, 40),
        'probabilite': 0.60
    },
    'Livret A': {
        'revenus_annuels': lambda: np.random.uniform(20, 80),
        'cout_gestion': lambda: 5,
        'probabilite': 0.45
    },
    'Assurance Vie': {
        'revenus_annuels': lambda: np.random.uniform(200, 800),  # Commissions
        'cout_gestion': lambda: np.random.uniform(50, 150),
        'probabilite': 0.30
    },
    'Crédit Immobilier': {
        'revenus_annuels': lambda: np.random.uniform(1500, 5000),  # Intérêts + frais
        'cout_gestion': lambda: np.random.uniform(300, 600),
        'probabilite': 0.25  # Pas tout le monde
    },
    'Crédit Consommation': {
        'revenus_annuels': lambda: np.random.uniform(300, 1200),
        'cout_gestion': lambda: np.random.uniform(80, 200),
        'probabilite': 0.20
    },
    'Assurance Habitation': {
        'revenus_annuels': lambda: np.random.uniform(150, 400),  # Primes
        'cout_gestion': lambda: np.random.uniform(50, 100),
        'probabilite': 0.40
    },
    'Assurance Auto': {
        'revenus_annuels': lambda: np.random.uniform(200, 600),
        'cout_gestion': lambda: np.random.uniform(60, 120),
        'probabilite': 0.50
    }
}

for idx, client_id in enumerate(client_ids):
    balance = balances[idx]
    emploi = emplois_clients[idx]
    age = ages[idx]
    
    # Ajuster les probabilités selon le profil client
    for produit, config in produits_bancaires.items():
        proba_base = config['probabilite']
        
        # Modifier probabilité selon profil
        if produit == 'Carte Bancaire Premium':
            proba = 0.8 if balance > 30000 else 0.1
        elif produit == 'Crédit Immobilier':
            proba = 0.5 if (age >= 30 and age <= 50 and emploi in ['Cadre', 'Profession libérale']) else 0.15
        elif produit == 'Assurance Vie':
            proba = 0.6 if balance > 20000 else 0.2
        elif produit == 'Livret A':
            proba = 0.7 if age < 30 else proba_base
        else:
            proba = proba_base
        
        # Souscrire ou non
        if random.random() < proba:
            revenus = config['revenus_annuels']()
            couts = config['cout_gestion']()
            
            produits_souscrits.append({
                'client_id': client_id,
                'produit': produit,
                'revenus_annuels': round(revenus, 2),
                'cout_gestion_annuel': round(couts, 2),
                'profit_annuel': round(revenus - couts, 2)
            })

df_produits = pd.DataFrame(produits_souscrits)

print(f"✅ {len(df_produits)} produits souscrits générés")
print(f"   Moyenne par client : {len(df_produits)/N_CLIENTS:.1f} produits")
print(f"   Profit moyen par produit : {df_produits['profit_annuel'].mean():.2f} €/an")

# ============================================================================
# PARTIE 4 : CALCUL RÉCAPITULATIF PAR CLIENT (pour vérification)
# ============================================================================

print("\n📊 Calcul de la rentabilité par client...")

# Agréger les revenus de transactions
revenus_transactions = df_transactions.groupby('client_id')['frais_generes'].sum().reset_index()
revenus_transactions.columns = ['client_id', 'revenus_transactions']

# Agréger les revenus/coûts des produits
revenus_produits = df_produits.groupby('client_id')['revenus_annuels'].sum().reset_index()
couts_produits = df_produits.groupby('client_id')['cout_gestion_annuel'].sum().reset_index()

# Fusionner avec la table clients
df_recap = df_clients[['client_id', 'cout_acquisition', 'anciennete_mois']].copy()
df_recap = df_recap.merge(revenus_transactions, on='client_id', how='left')
df_recap = df_recap.merge(revenus_produits, on='client_id', how='left')
df_recap = df_recap.merge(couts_produits, on='client_id', how='left')

# Remplacer NaN par 0
df_recap = df_recap.fillna(0)

# Calculer profit total
# Revenus = transactions + produits annuels
# Coûts = acquisition (amortis sur ancienneté) + coûts produits
df_recap['revenus_totaux'] = df_recap['revenus_transactions'] + df_recap['revenus_annuels']
df_recap['couts_totaux'] = (df_recap['cout_acquisition'] / (df_recap['anciennete_mois'] + 1)) + df_recap['cout_gestion_annuel']
df_recap['profit_net'] = df_recap['revenus_totaux'] - df_recap['couts_totaux']

# Segmenter les clients
def segmenter_client(profit):
    if profit > 500:
        return 'VIP'
    elif profit > 0:
        return 'Standard'
    else:
        return 'Déficitaire'

df_recap['segment_calcule'] = df_recap['profit_net'].apply(segmenter_client)

print(f"\n✅ Analyse de rentabilité calculée :")
print(f"   Profit moyen par client : {df_recap['profit_net'].mean():.2f} €")
print(f"   Profit médian : {df_recap['profit_net'].median():.2f} €")
print(f"\n   Segmentation :")
print(df_recap['segment_calcule'].value_counts())
print(f"\n   Profit total banque : {df_recap['profit_net'].sum():.2f} €")

# ============================================================================
# PARTIE 5 : EXPORT DES FICHIERS CSV
# ============================================================================

print("\n💾 Export des fichiers CSV...")

# Exporter les 3 tables principales
df_clients.to_csv('clients.csv', index=False, encoding='utf-8')
df_transactions.to_csv('transactions.csv', index=False, encoding='utf-8')
df_produits.to_csv('produits_souscrits.csv', index=False, encoding='utf-8')

# Exporter aussi le récap pour vérification (optionnel)
df_recap.to_csv('recap_rentabilite.csv', index=False, encoding='utf-8')

print("✅ Fichiers exportés avec succès :")
print("   - clients.csv")
print("   - transactions.csv")
print("   - produits_souscrits.csv")
print("   - recap_rentabilite.csv (fichier de vérification)")

# ============================================================================
# PARTIE 6 : APERÇU DES DONNÉES
# ============================================================================

print("\n" + "="*80)
print("📊 APERÇU DES DONNÉES GÉNÉRÉES")
print("="*80)

print("\n1️⃣ TABLE CLIENTS (5 premières lignes) :")
print(df_clients.head())

print("\n2️⃣ TABLE TRANSACTIONS (5 premières lignes) :")
print(df_transactions.head())

print("\n3️⃣ TABLE PRODUITS SOUSCRITS (5 premières lignes) :")
print(df_produits.head())

print("\n" + "="*80)
print("🎉 GÉNÉRATION TERMINÉE AVEC SUCCÈS !")
print("="*80)
print("\nProchaines étapes :")
print("1. Charge ces fichiers CSV dans DuckDB")
print("2. Commence ton analyse SQL")
print("3. Crée ton dashboard Power BI")
print("\nBon courage ! 💪")
