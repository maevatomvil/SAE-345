#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
    SELECT ligne_panier.telephone_id, ligne_panier.quantite, 
           telephone.nom_telephone AS nom_telephone,  
           COALESCE(ligne_panier.prix_unitaire, telephone.prix_telephone) AS prix_telephone,
           COALESCE(declinaison_telephone.stock, telephone.stock) AS stock,  
           (ligne_panier.quantite * COALESCE(ligne_panier.prix_unitaire, telephone.prix_telephone)) AS prix_ligne,
           ligne_panier.declinaison_id,
           declinaison_telephone.taille,
           couleur.libelle_couleur
    FROM ligne_panier
    JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
    LEFT JOIN declinaison_telephone ON ligne_panier.declinaison_id = declinaison_telephone.id_declinaison
    LEFT JOIN couleur ON declinaison_telephone.couleur_id = couleur.id_couleur
    WHERE ligne_panier.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    telephone_panier = mycursor.fetchall()
    
    prix_total = None
    nombre_articles = 0
    if len(telephone_panier) >= 1:
        sql = '''
        SELECT SUM(ligne_panier.quantite * COALESCE(ligne_panier.prix_unitaire, telephone.prix_telephone)) AS prix_total,
               SUM(ligne_panier.quantite) AS nombre_articles
        FROM ligne_panier
        JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
        LEFT JOIN declinaison_telephone ON ligne_panier.declinaison_id = declinaison_telephone.id_declinaison
        WHERE ligne_panier.utilisateur_id = %s
        '''
        mycursor.execute(sql, (id_client,))
        result = mycursor.fetchone()
        prix_total = result['prix_total']
        nombre_articles = result['nombre_articles']
    # etape 2 : selection des adresses

    sql = '''SELECT id_adresse, rue, ville, code_postal FROM adresse WHERE utilisateur_id = %s'''
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()

    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , telephone_panier=telephone_panier
                           , prix_total=prix_total
                           , nombre_articles=nombre_articles
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    id_client = session['id_user']
    id_adresse_livraison = request.form.get("id_adresse_livraison", "")
    id_adresse_facturation = request.form.get("id_adresse_facturation", "")

    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas de télephones dans le panier', 'alert-warning')
        return redirect('/client/telephone/show')
    
    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande, id_client, '1', id_adresse_facturation, id_adresse_livraison)
    sql = "INSERT INTO commande(date_achat, utilisateur_id, etat_id, adresse_facturation_id, adresse_livraison_id) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(sql, tuple_insert)
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()
    print(commande_id, tuple_insert)

    for item in items_ligne_panier:
        sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND telephone_id = %s"
        if item['declinaison_id'] is not None:
            sql += " AND declinaison_id = %s"
            mycursor.execute(sql, (item['utilisateur_id'], item['telephone_id'], item['declinaison_id']))
        else:
            sql += " AND declinaison_id IS NULL"
            mycursor.execute(sql, (item['utilisateur_id'], item['telephone_id']))
        
        # Utiliser le prix unitaire stocké dans le panier ou prix du téléphone
        prix_unitaire = item['prix_unitaire'] if item['prix_unitaire'] is not None else None
        
        if prix_unitaire is None:
            sql = "SELECT prix_telephone AS prix FROM telephone WHERE id_telephone = %s"
            mycursor.execute(sql, item['telephone_id'])
            prix_data = mycursor.fetchone()
            prix_unitaire = prix_data['prix']
            
        # Insérer la ligne de commande avec la déclinaison si présente
        if item['declinaison_id'] is not None:
            sql = "INSERT INTO ligne_commande(commande_id, telephone_id, prix, quantite, declinaison_id) VALUES (%s, %s, %s, %s, %s)"
            tuple_insert = (commande_id['last_insert_id'], item['telephone_id'], prix_unitaire, item['quantite'], item['declinaison_id'])
        else:
            sql = "INSERT INTO ligne_commande(commande_id, telephone_id, prix, quantite) VALUES (%s, %s, %s, %s)"
            tuple_insert = (commande_id['last_insert_id'], item['telephone_id'], prix_unitaire, item['quantite'])
            
        mycursor.execute(sql, tuple_insert)

    sql = "UPDATE adresse SET favori = 0 WHERE utilisateur_id = %s"
    mycursor.execute(sql, id_client)

    sql = "UPDATE adresse SET favori = 1 WHERE id_adresse = %s"
    mycursor.execute(sql, id_adresse_livraison)

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/telephone/show')

@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    mycursor.execute("SELECT * FROM ligne_commande")
    print(mycursor.fetchall())

    sql = """SELECT commande.id_commande, commande.date_achat, COUNT(ligne_commande.telephone_id) AS nbr_telephones, SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total, commande.etat_id, etat.libelle 
             FROM commande
             JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
             JOIN etat ON commande.etat_id = etat.id_etat
             WHERE utilisateur_id = %s
             GROUP BY commande.id_commande, commande.date_achat, commande.etat_id, etat.libelle
             ORDER BY commande.date_achat;"""
    mycursor.execute(sql, id_client)
    commandes = mycursor.fetchall()

    print(commandes)
    telephones_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = '''SELECT ligne_commande.*, telephone.nom_telephone AS nom, 
                 (ligne_commande.prix * ligne_commande.quantite) AS prix_ligne,
                 ligne_commande.declinaison_id,
                 declinaison_telephone.taille,
                 couleur.libelle_couleur
                 FROM ligne_commande
                 JOIN telephone ON ligne_commande.telephone_id = telephone.id_telephone
                 LEFT JOIN declinaison_telephone ON ligne_commande.declinaison_id = declinaison_telephone.id_declinaison
                 LEFT JOIN couleur ON declinaison_telephone.couleur_id = couleur.id_couleur
                 WHERE ligne_commande.commande_id = %s'''
        mycursor.execute(sql, id_commande)
        telephones_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = '''SELECT commande.adresse_livraison_id, adresse.rue AS rue_livraison, adresse.code_postal AS code_postal_livraison, adresse.ville as ville_livraison
                 FROM commande
                 JOIN adresse on commande.adresse_livraison_id = adresse.id_adresse
                 WHERE commande.id_commande = %s'''
        mycursor.execute(sql, id_commande)
        adresse_livraison = mycursor.fetchone()

        sql = '''SELECT commande.adresse_facturation_id, adresse.rue AS rue_facturation, adresse.code_postal AS code_postal_facturation, adresse.ville as ville_facturation
                 FROM commande
                 JOIN adresse on commande.adresse_facturation_id = adresse.id_adresse
                 WHERE commande.id_commande = %s'''
        mycursor.execute(sql, id_commande)
        adresse_facturation = mycursor.fetchone()

        commande_adresses = dict(list(adresse_livraison.items()) + list(adresse_facturation.items()))

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , telephones_commande=telephones_commande
                           , commande_adresses=commande_adresses
                           )

