#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, Flask, request, render_template, redirect, url_for, flash, session
from connexion_db import get_db

client_telephone = Blueprint('client_telephone', __name__, template_folder='templates')

@client_telephone.route('/client/index')
@client_telephone.route('/client/telephone/show', methods=['GET', 'POST'])
def client_telephone_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    if request.method == 'POST':
        filter_word = request.form.get('filter_word', '').strip()
        filter_prix_min = request.form.get('filter_prix_min', '')
        filter_prix_max = request.form.get('filter_prix_max', '')
        filter_types_raw = request.form.getlist('filter_types[]')

        filter_types = []
        for item in filter_types_raw:
            if isinstance(item, str) and item.isdigit():
                filter_types.append(int(item))

        try:
            filter_prix_min = float(filter_prix_min) if filter_prix_min else None
        except ValueError:
            filter_prix_min = None
            flash("Le prix minimum n'est pas valide.", "alert-warning")

        try:
            filter_prix_max = float(filter_prix_max) if filter_prix_max else None
        except ValueError:
            filter_prix_max = None
            flash("Le prix maximum n'est pas valide.", "alert-warning")

        session['filter_word'] = filter_word
        session['filter_prix_min'] = filter_prix_min
        session['filter_prix_max'] = filter_prix_max
        session['filter_types'] = filter_types
    else:
        filter_word = session.get('filter_word', '')
        filter_prix_min = session.get('filter_prix_min')
        filter_prix_max = session.get('filter_prix_max')
        filter_types = session.get('filter_types', [])

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
              telephone.image AS image,
              (SELECT COUNT(*) FROM declinaison_telephone WHERE telephone_id = telephone.id_telephone) AS nombre_declinaisons,
              (SELECT COALESCE(SUM(stock), telephone.stock) 
               FROM declinaison_telephone 
               WHERE telephone_id = telephone.id_telephone) AS stock_total,
              (SELECT GROUP_CONCAT(
                    CONCAT(taille, ' (', stock, ')')
                    ORDER BY taille
                    SEPARATOR ' | '
               )
               FROM declinaison_telephone 
               WHERE telephone_id = telephone.id_telephone) AS details_stock
       FROM telephone
       JOIN couleur ON telephone.couleur_id = couleur.id_couleur
       JOIN type_telephone ON telephone.type_telephone_id = type_telephone.id_type_telephone
       WHERE 1=1
    '''
    params = []

    if filter_word:
        sql += " AND (telephone.nom_telephone LIKE %s OR type_telephone.libelle_type_telephone LIKE %s)"
        params.extend((f"%{filter_word}%", f"%{filter_word}%"))

    if filter_prix_min is not None:
        sql += " AND telephone.prix_telephone >= %s"
        params.append(filter_prix_min)

    if filter_prix_max is not None:
        sql += " AND telephone.prix_telephone <= %s"
        params.append(filter_prix_max)

    if filter_types:
        sql += " AND telephone.type_telephone_id IN ({})".format(",".join(["%s"] * len(filter_types)))
        params.extend(filter_types)

    sql += " ORDER BY telephone.nom_telephone"

    mycursor.execute(sql, params)
    telephones = mycursor.fetchall()

    if not telephones:
        flash("Aucun téléphone ne correspond à votre sélection.", "alert-warning")

    mycursor.execute('''
        SELECT id_type_telephone, libelle_type_telephone as libelle
        FROM type_telephone 
        ORDER BY libelle_type_telephone;
    ''')
    types_telephone = mycursor.fetchall()

    mycursor.execute('''
        SELECT ligne_panier.telephone_id AS id_telephone, ligne_panier.quantite, 
               telephone.nom_telephone AS nom_telephone,  
               COALESCE(declinaison_telephone.prix, telephone.prix_telephone) AS prix_telephone,
               COALESCE(declinaison_telephone.stock, telephone.stock) AS stock,  
               (ligne_panier.quantite * COALESCE(declinaison_telephone.prix, telephone.prix_telephone)) AS prix_ligne,
               declinaison_telephone.taille,
               couleur.libelle_couleur,
               ligne_panier.declinaison_id,
               ligne_panier.prix_unitaire
        FROM ligne_panier
        JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
        LEFT JOIN declinaison_telephone ON ligne_panier.declinaison_id = declinaison_telephone.id_declinaison
        LEFT JOIN couleur ON declinaison_telephone.couleur_id = couleur.id_couleur
        WHERE ligne_panier.utilisateur_id = %s;
    ''', (id_client,))
    telephones_panier = mycursor.fetchall()

    prix_total = None
    if telephones_panier:
        mycursor.execute('''
            SELECT SUM(ligne_panier.quantite * COALESCE(ligne_panier.prix_unitaire, telephone.prix_telephone)) AS prix_total
            FROM ligne_panier
            JOIN telephone ON ligne_panier.telephone_id = telephone.id_telephone
            LEFT JOIN declinaison_telephone ON ligne_panier.declinaison_id = declinaison_telephone.id_declinaison
            WHERE ligne_panier.utilisateur_id = %s;
        ''', (id_client,))
        result = mycursor.fetchone()
        prix_total = result['prix_total']

    return render_template('client/boutique/panier_telephone.html',
                           telephones=telephones,
                           telephone_panier=telephones_panier,
                           prix_total=prix_total,
                           items_filtre=types_telephone,
                           filter_word=filter_word,
                           filter_prix_min=filter_prix_min,
                           filter_prix_max=filter_prix_max,
                           filter_types=filter_types)