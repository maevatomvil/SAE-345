#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone')
    quantite = request.form.get('quantite')
    id_declinaison = request.form.get('id_declinaison')

    # Si l'ID de déclinaison n'est pas fourni, on vérifie s'il y a des déclinaisons
    if not id_declinaison:
        # Vérifier le nombre de déclinaisons disponibles
        sql = '''
            SELECT COUNT(*) as nb_declinaisons,
                   (SELECT id_declinaison FROM declinaison_telephone WHERE telephone_id = %s LIMIT 1) as premiere_declinaison
            FROM declinaison_telephone 
            WHERE telephone_id = %s
        '''
        mycursor.execute(sql, (id_telephone, id_telephone))
        result = mycursor.fetchone()
        
        if result['nb_declinaisons'] == 0:
            # Pas de déclinaisons, on ajoute directement au panier
            id_declinaison = None
        elif result['nb_declinaisons'] == 1:
            # Une seule déclinaison, on l'utilise directement
            id_declinaison = result['premiere_declinaison']
        else:
            # Plusieurs déclinaisons, on affiche la page de sélection
            sql = '''
                SELECT t.id_telephone, t.nom_telephone, t.prix_telephone, t.image, 
                       d.id_declinaison, d.taille, d.stock, d.prix, d.couleur_id,
                       c.libelle_couleur, c.id_couleur
                FROM telephone t
                JOIN declinaison_telephone d ON t.id_telephone = d.telephone_id
                LEFT JOIN couleur c ON d.couleur_id = c.id_couleur
                WHERE t.id_telephone = %s
                AND d.stock > 0
                ORDER BY d.prix ASC, c.libelle_couleur ASC
            '''
            mycursor.execute(sql, (id_telephone,))
            declinaisons = mycursor.fetchall()
            
            if not declinaisons:
                flash(u'Aucune déclinaison disponible pour ce téléphone')
                return redirect('/client/telephone/show')
                
            # On extrait les infos du téléphone de la première déclinaison
            telephone = {
                'id_telephone': declinaisons[0]['id_telephone'],
                'nom_telephone': declinaisons[0]['nom_telephone'],
                'prix_telephone': declinaisons[0]['prix_telephone'],
                'image': declinaisons[0]['image']
            }
            
            return render_template('client/boutique/declinaison_telephone.html',
                               telephone=telephone,
                               declinaisons=declinaisons,
                               quantite=quantite)

    # Vérifier le stock de la déclinaison sélectionnée
    if id_declinaison:
        sql = "SELECT stock, prix FROM declinaison_telephone WHERE id_declinaison = %s"
        mycursor.execute(sql, (id_declinaison,))
        declinaison = mycursor.fetchone()
        
        if declinaison and declinaison['stock'] >= int(quantite):
            # Mettre à jour le stock de la déclinaison
            sql = "UPDATE declinaison_telephone SET stock = stock - %s WHERE id_declinaison = %s"
            mycursor.execute(sql, (quantite, id_declinaison))
            
            # Récupérer les infos complètes de la déclinaison pour le panier
            sql = '''
                SELECT t.id_telephone, t.nom_telephone, d.taille, c.libelle_couleur, d.prix
                FROM declinaison_telephone d
                JOIN telephone t ON d.telephone_id = t.id_telephone
                LEFT JOIN couleur c ON d.couleur_id = c.id_couleur
                WHERE d.id_declinaison = %s
            '''
            mycursor.execute(sql, (id_declinaison,))
            info_declinaison = mycursor.fetchone()
            
            # Créer un nom complet pour l'affichage dans le panier
            nom_complet = info_declinaison['nom_telephone']
            if info_declinaison['taille']:
                nom_complet += f" ({info_declinaison['taille']})"
            if info_declinaison['libelle_couleur']:
                nom_complet += f" - {info_declinaison['libelle_couleur']}"
                
            # Utiliser le prix de la déclinaison, pas celui du téléphone de base
            prix_declinaison = info_declinaison['prix']
        else:
            flash(u'Stock insuffisant pour cette déclinaison')
            return redirect('/client/telephone/show')
    else:
        # Vérifier le stock du téléphone principal
        sql = "SELECT stock FROM telephone WHERE id_telephone = %s"
        mycursor.execute(sql, (id_telephone,))
        stock_telephone = mycursor.fetchone()
        if stock_telephone and stock_telephone['stock'] >= int(quantite):
            # Mettre à jour le stock du téléphone
            sql = "UPDATE telephone SET stock = stock - %s WHERE id_telephone = %s"
            mycursor.execute(sql, (quantite, id_telephone))
        else:
            flash(u'Stock insuffisant')
            return redirect('/client/telephone/show')

    # Ajouter au panier
    if id_declinaison:
        # Pour les articles avec déclinaison, utiliser ID déclinaison comme clé
        sql = "SELECT * FROM ligne_panier WHERE telephone_id = %s AND utilisateur_id = %s AND declinaison_id = %s"
        mycursor.execute(sql, (id_telephone, id_client, id_declinaison))
    else:
        # Pour les articles sans déclinaison, utiliser juste ID téléphone comme clé
        sql = "SELECT * FROM ligne_panier WHERE telephone_id = %s AND utilisateur_id = %s AND declinaison_id IS NULL"
        mycursor.execute(sql, (id_telephone, id_client))
    
    telephone_panier = mycursor.fetchone()
    
    # Si on utilise une déclinaison, ajouter les informations de déclinaison
    prix_panier = None
    if id_declinaison:
        # Utiliser le prix de la déclinaison
        prix_panier = prix_declinaison
    else:
        # Utiliser le prix du téléphone principal
        sql = "SELECT prix_telephone FROM telephone WHERE id_telephone = %s"
        mycursor.execute(sql, (id_telephone,))
        prix_panier = mycursor.fetchone()['prix_telephone']

    if telephone_panier and telephone_panier['quantite'] >= 1:
        # Mise à jour d'une ligne existante
        if id_declinaison:
            sql = "UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND telephone_id = %s AND declinaison_id = %s"
            mycursor.execute(sql, (quantite, id_client, id_telephone, id_declinaison))
        else:
            sql = "UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND telephone_id = %s AND declinaison_id IS NULL"
            mycursor.execute(sql, (quantite, id_client, id_telephone))
    else:
        # Création d'une nouvelle ligne
        if id_declinaison:
            sql = """
                INSERT INTO ligne_panier(utilisateur_id, telephone_id, quantite, date_ajout, declinaison_id, prix_unitaire) 
                VALUES (%s, %s, %s, current_timestamp, %s, %s)
            """
            mycursor.execute(sql, (id_client, id_telephone, quantite, id_declinaison, prix_panier))
        else:
            sql = """
                INSERT INTO ligne_panier(utilisateur_id, telephone_id, quantite, date_ajout, prix_unitaire) 
                VALUES (%s, %s, %s, current_timestamp, %s)
            """
            mycursor.execute(sql, (id_client, id_telephone, quantite, prix_panier))

    get_db().commit()
    flash(u'Article ajouté au panier')
    return redirect('/client/telephone/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone', '')
    id_declinaison = request.form.get('id_declinaison')
    quantite = 1
    
    # Récupérer la ligne du panier
    if id_declinaison:
        sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id=%s"
        mycursor.execute(sql, (id_client, id_telephone, id_declinaison))
    else:
        sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id IS NULL"
        mycursor.execute(sql, (id_client, id_telephone))
    
    telephone_panier = mycursor.fetchone()

    if telephone_panier and telephone_panier['quantite'] > 1:
        # Diminuer la quantité
        if id_declinaison:
            sql = "UPDATE ligne_panier SET quantite = quantite-%s WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id=%s"
            mycursor.execute(sql, (quantite, id_client, id_telephone, id_declinaison))
        else:
            sql = "UPDATE ligne_panier SET quantite = quantite-%s WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id IS NULL"
            mycursor.execute(sql, (quantite, id_client, id_telephone))
    else:
        # Supprimer la ligne
        if id_declinaison:
            sql = "DELETE FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id=%s"
            mycursor.execute(sql, (id_client, id_telephone, id_declinaison))
        else:
            sql = "DELETE FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id IS NULL"
            mycursor.execute(sql, (id_client, id_telephone))

    # Mise à jour du stock
    if id_declinaison:
        sql = "UPDATE declinaison_telephone SET stock = stock + %s WHERE id_declinaison = %s"
        mycursor.execute(sql, (quantite, id_declinaison))
    else:
        sql = "UPDATE telephone SET stock = stock + %s WHERE id_telephone = %s"
        mycursor.execute(sql, (quantite, id_telephone))

    get_db().commit()
    return redirect('/client/telephone/show')

@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    
    # Récupérer toutes les lignes du panier
    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()
    
    for item in items_panier:
        # Remettre en stock
        if item['declinaison_id'] is not None:
            # Remettre en stock dans la déclinaison
            sql = "UPDATE declinaison_telephone SET stock = stock + %s WHERE id_declinaison = %s"
            mycursor.execute(sql, (item['quantite'], item['declinaison_id']))
        else:
            # Remettre en stock dans le téléphone principal
            sql = "UPDATE telephone SET stock = stock + %s WHERE id_telephone = %s"
            mycursor.execute(sql, (item['quantite'], item['telephone_id']))
    
    # Vider le panier
    sql = "DELETE FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql, (id_client,))
    
    get_db().commit()
    return redirect('/client/telephone/show')

@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone', '')
    id_declinaison = request.form.get('id_declinaison')

    # Récupérer la ligne du panier
    if id_declinaison:
        sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id=%s"
        mycursor.execute(sql, (id_client, id_telephone, id_declinaison))
    else:
        sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id IS NULL"
        mycursor.execute(sql, (id_client, id_telephone))
    
    ligne_panier = mycursor.fetchone()

    if ligne_panier:
        quantite = ligne_panier['quantite']

        # Supprimer la ligne
        if id_declinaison:
            sql = "DELETE FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id=%s"
            mycursor.execute(sql, (id_client, id_telephone, id_declinaison))
            
            # Remettre en stock
            sql = "UPDATE declinaison_telephone SET stock = stock + %s WHERE id_declinaison = %s"
            mycursor.execute(sql, (quantite, id_declinaison))
        else:
            sql = "DELETE FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s AND declinaison_id IS NULL"
            mycursor.execute(sql, (id_client, id_telephone))
            
            # Remettre en stock
            sql = "UPDATE telephone SET stock = stock + %s WHERE id_telephone = %s"
            mycursor.execute(sql, (quantite, id_telephone))

        get_db().commit()

    return redirect('/client/telephone/show')

@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    try:
        session['filter_prix_min'] = float(filter_prix_min) if filter_prix_min else None
        session['filter_prix_max'] = float(filter_prix_max) if filter_prix_max else None
    except ValueError:
        flash("Erreur: Les valeurs de prix doivent être numériques", "alert-danger")
    # mise en session des variables
    session['filter_word'] = filter_word if filter_word else None
    session['filter_types'] = filter_types if filter_types else None

    flash("Filtres appliqués avec succès", "alert-info")
    return redirect('/client/telephone/show')

@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    flash("Filtres réinitialisés", "alert-danger")
    return redirect('/client/telephone/show')
