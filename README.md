Bienvenue dans le projet SAE — E-commerce Téléphones
🎯 Objectifb

Créer un site e-commerce de vente de téléphones avec gestion client et admin.
Les fonctionnalités incluent :

    Espace client : inscription, navigation, filtrage, panier, commandes, commentaires, wishlist.

    Espace admin : gestion des téléphones, types, déclinaisons, commandes, commentaires, statistiques.

📁 Structure du projet

🧠 Très important :

    TOUS les fichiers nécessaires sont déjà créés.
    ✅ Tu n’as PAS besoin d’en créer d’autres.
    🔍 Tu dois chercher le bon fichier et modifier son code.

🔧 Fichier principal
Fichier	Rôle
app.py	Démarre l’app Flask, gère la sécurité, redirige les utilisateurs, et connecte les routes (blueprints)
🔐 Authentification
Fichier	Rôle
auth_security.py	Connexion / inscription / déconnexion / hachage des mots de passe
🧪 Chargement de la base
Fichier	Rôle
fixtures_load.py	Remplit la base avec les données du fichier sae_sql.sql (pour les tests)
sae_sql.sql	Le script SQL complet avec tables + données
🧰 Connexion BDD
Fichier	Rôle
connexion_db.py	Connecte MySQL et gère le curseur
🛍️ Fonctionnalités Client
Fichier	Rôle
client_telephone.py	Affiche les téléphones avec filtres, détails et panier
client_panier.py	Ajoute, supprime et vide le panier
client_commande.py	Gère la validation et le suivi des commandes
client_commentaire.py	Gère les avis/commentaires/notes
client_coordonnee.py	Gère les informations personnelles et les adresses
client_liste_envies.py	Wishlist (liste d’envies)
🛠️ Fonctionnalités Admin
Fichier	Rôle
admin_telephone.py	Ajouter, modifier, supprimer un téléphone (CRUD)
admin_type_telephone.py	Gérer les types de téléphone
admin_declinaison_telephone.py	Gérer les déclinaisons (taille, couleur, stock)
admin_commande.py	Voir et valider les commandes clients
admin_dataviz.py	Affichage des statistiques (stocks, adresses, etc.)
admin_commentaire.py	Modérer les commentaires, répondre, supprimer
✅ Règles de codage à suivre (niveau étudiant)
1. ✨ Garde un code clair et propre

    Écris simplement, comme si tu allais réexpliquer ton code à un camarade

    Pas de blocs de code trop longs

    Structure et indentation : très important

2. 📌 Pas de création de nouveaux fichiers

    Tous les fichiers sont déjà bien organisés.
    🔍 Il faut chercher le bon fichier et modifier dedans.

Par exemple :

    Tu veux modifier l'affichage des téléphones pour les clients ? ➤ C’est dans client_telephone.py et templates/client/boutique/

    Tu veux changer le panier ? ➤ Va dans client_panier.py

    Tu veux gérer les types ? ➤ Va dans admin_type_telephone.py

3. 🧼 Nomme bien tes variables

Exemples :

id_telephone
prix_total
login_utilisateur

Pas de noms comme x, data, truc, info1…
4. 💬 Ajoute des commentaires utiles

TES NOUVEAUX COMMENTAIRE COMMENCE LES AVEC ###################### comme ça tjr
# Mise à jour du stock après ajout au panier

5. 🔎 Utilise le SQL pour les calculs

Tu dois faire les calculs (somme, moyenne, etc.) dans la requête SQL, jamais en Python.
6. 🚫 Ce qu’il ne faut jamais faire
❌ Ne pas faire	✅ À la place
url_for()	Utiliser les routes en dur (/client/telephone/show)
try / except	Éviter toute gestion d’erreur pour ce projet
Calcul en Python (somme, etc.)	Faire en SQL
Boucles dans app.py	Gérer ça dans d’autres fichiers
JavaScript	Aucune utilisation autorisée
Créer de nouveaux fichiers	Modifier les fichiers existants
🛠️ Méthode pour ajouter une fonctionnalité

    Comprendre le besoin (par exemple : ajouter un filtre)

    Identifier le fichier concerné (ex : client_telephone.py)

    Modifier la requête SQL si nécessaire

    Modifier la vue HTML correspondante dans templates/

    Tester dans le navigateur

    Demander une relecture à un camarade si possible


    si t'as besoin d excuter un truc sur sql utulise : # mysql --user=login --password=secret --host=serveurmysql --database=BDD_login
