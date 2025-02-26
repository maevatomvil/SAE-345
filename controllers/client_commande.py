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
           telephone.prix_telephone AS prix_telephone,
           telephone.stock AS stock,  
           (ligne_panier.quantite * telephone.prix_telephone) AS prix_ligne
    FROM ligne_panier
    JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
    WHERE ligne_panier.utilisateur_id = %s
    '''
    mycursor.execute(sql, (id_client,))
    telephones_panier = mycursor.fetchall()
    prix_total = None
    if len(telephones_panier) >= 1:
        sql = '''
        SELECT SUM(ligne_panier.quantite * telephone.prix_telephone) AS prix_total
        FROM ligne_panier
        JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
        WHERE ligne_panier.utilisateur_id = %s
        '''
        mycursor.execute(sql, (id_client,))
        result = mycursor.fetchone()
        prix_total = result['prix_total']
    # etape 2 : selection des adresses

    #sql = '''SELECT commande.adresse_livraison_id, adresse.rue, adresse.code_postal, adresse.ville
    #            FROM commande
    #            JOIN adresse on commande.adresse_livraison_id = adresse.id_adresse
    #            WHERE commande.id_commande = %s'''
    #mycursor.execute(sql, id_commande)
    #adresse_livraison = mycursor.fetchall()

    commande_adresses = dict(list(adresse_livraison.items()) + list(adresse_facturation.items()))

    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , telephones_panier=telephones_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    id_client = session['id_user']

    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas de télephones dans le panier', 'alert-warning')
        return redirect('/client/telephone/show')
    
    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande, id_client, '1')
    sql = "INSERT INTO commande(date_achat, utilisateur_id, etat_id) VALUES (%s, %s, %s)"
    mycursor.execute(sql, tuple_insert)
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()
    print(commande_id, tuple_insert)

    for item in items_ligne_panier:
        sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND telephone_id = %s"
        mycursor.execute(sql, (item['utilisateur_id'], item['telephone_id']))
        sql = "SELECT prix_telephone AS prix FROM telephone WHERE id_telephone = %s"
        mycursor.execute(sql, item['telephone_id'])
        prix = mycursor.fetchone()
        print(prix)
        sql = "INSERT INTO ligne_commande(commande_id, telephone_id, prix, quantite) VALUES (%s, %s, %s, %s)"
        tuple_insert = (commande_id['last_insert_id'], item['telephone_id'], prix['prix'], item['quantite'])
        print(tuple_insert)
        mycursor.execute(sql, tuple_insert)

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
        sql = ''' selection du détails d'une commande '''
        sql = '''SELECT ligne_commande.*, telephone.nom_telephone AS nom, SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_ligne
                 FROM ligne_commande
                 JOIN telephone ON ligne_commande.telephone_id = telephone.id_telephone
                 WHERE ligne_commande.commande_id = %s
                 GROUP BY ligne_commande.commande_id, ligne_commande.telephone_id, ligne_commande.prix, ligne_commande.quantite'''
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

