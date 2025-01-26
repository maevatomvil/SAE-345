#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_telephone = Blueprint('client_telephone', __name__,
                        template_folder='templates')

@client_telephone.route('/client/index')
@client_telephone.route('/client/telephone/show')              # remplace /client
def client_telephone_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''   
       SELECT id_telephone AS id_telephone
               , nom_telephone AS nom
               , prix_telephone AS prix
               , poids AS poids
               , taille AS taille
               , libelle_couleur AS couleur
               , libelle_type_telephone AS type
        FROM telephone
        JOIN couleur ON telephone.couleur_id = couleur.id_couleur
        JOIN type_telephone ON telephone.type_telephone_id = type_telephone.id_type_telephone
        ORDER BY nom_telephone;'''
    mycursor.execute(sql)
    telephones = mycursor.fetchall()

    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    sql = '''SELECT * FROM telephone;'''
    mycursor.execute(sql)
    telephone = mycursor.fetchall()
    telephones = telephone


    # pour le filtre
    types_telephone = []
    sql = '''
    SELECT id_type_telephone, libelle_type_telephone as libelle
    FROM type_telephone 
    ORDER BY libelle_type_telephone;
    '''
    mycursor.execute(sql)
    types_telephone = mycursor.fetchall()

    telephones_panier = []

    if len(telephones_panier) >= 1:
        sql = ''' SELECT SUM(ligne_panier.quantite * telephone.prix_telephone) AS prix_total
            FROM ligne_panier
            JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
            WHERE ligne_panier.utilisateur_id = %s; '''
        mycursor.execute(sql, (id_client))
        result = mycursor.fetchone()
        prix_total = result['prix_total']
    else:
        prix_total = None
    return render_template('client/boutique/panier_telephone.html'
                           , telephones=telephones
                           , telephones_panier=telephones_panier
                           , prix_total=prix_total
                           , items_filtre=types_telephone
                           )
