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
       SELECT telephone.id_telephone AS id_telephone,
              telephone.nom_telephone AS nom_telephone,  
              telephone.prix_telephone AS prix_telephone,  
              telephone.poids AS poids,
              telephone.taille AS taille,
              couleur.libelle_couleur AS couleur,
              type_telephone.libelle_type_telephone AS type,
              telephone.fournisseur AS fournisseur,
              telephone.marque AS marque,
              telephone.stock AS stock,
              telephone.image AS image
       FROM telephone
       JOIN couleur ON telephone.couleur_id = couleur.id_couleur
       JOIN type_telephone ON telephone.type_telephone_id = type_telephone.id_type_telephone
       ORDER BY telephone.nom_telephone;
    '''
    mycursor.execute(sql)
    telephones = mycursor.fetchall()
    filter_word = session.get('filter_word', '')
    filter_prix_min = session.get('filter_prix_min')
    filter_prix_max = session.get('filter_prix_max')
    filter_types = session.get('filter_types', [])

    if filter_word or filter_prix_min is not None or filter_prix_max is not None or filter_types:
        telephones_filtres = []

        for tel in telephones:
            match = True
            if filter_word and not (filter_word.lower() in tel["nom_telephone"].lower() or filter_word.lower() in tel["type"].lower()):
                match = False
            if filter_prix_min is not None and tel["prix_telephone"] < filter_prix_min:
                match = False
            if filter_prix_max is not None and tel["prix_telephone"] > filter_prix_max:
                match = False
            if filter_types and tel["id_type"] not in filter_types:
                match = False

            if match:
                telephones_filtres.append(tel)

        if telephones_filtres:
            telephones = telephones_filtres

    print(telephones)

    # utilisation du filtre
    sql = '''SELECT * FROM telephone;'''
    mycursor.execute(sql)
    telephone = mycursor.fetchall()
    telephones = telephone


    # pour le filtre
    sql = '''
    SELECT id_type_telephone, libelle_type_telephone as libelle
    FROM type_telephone 
    ORDER BY libelle_type_telephone;
    '''
    mycursor.execute(sql)
    types_telephone = mycursor.fetchall()

    #pour le panier

    sql = '''
    SELECT ligne_panier.telephone_id,
    ligne_panier.quantite,
    telephone.nom_telephone,
    telephone.prix_telephone,
    telephone.stock,
    couleur.id_couleur,
    couleur.libelle_couleur,
    telephone.taille
    FROM ligne_panier
    JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
    LEFT JOIN couleur ON telephone.couleur_id = couleur.id_couleur
    WHERE ligne_panier.utilisateur_id = %s;
    '''

    mycursor.execute(sql, (id_client,))
    telephone_panier = mycursor.fetchall()

    if len(telephone_panier) >= 1:
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
                           , telephone_panier=telephone_panier
                           , prix_total=prix_total
                           , items_filtre=types_telephone,
                            filter_word = filter_word,
                            filter_prix_min = filter_prix_min,
                            filter_prix_max = filter_prix_max,
                            filter_types = filter_types
                           )
