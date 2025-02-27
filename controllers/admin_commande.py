#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                           template_folder='templates')


@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']

    sql = '''SELECT commande.id_commande, commande.date_achat, 
             utilisateur.login, COUNT(ligne_commande.telephone_id) AS nbr_telephones, 
             SUM(ligne_commande.prix * ligne_commande.quantite) AS prix_total, 
             commande.etat_id, etat.libelle 
             FROM commande
             JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
             JOIN etat ON commande.etat_id = etat.id_etat
             JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
             GROUP BY commande.id_commande, commande.date_achat, commande.utilisateur_id, 
                     utilisateur.login, commande.etat_id, etat.libelle
             ORDER BY commande.date_achat DESC;'''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    telephones_commande = None
    commande_adresses = None
    adresse_livraison = None
    adresse_facturation = None

    id_commande = request.args.get('id_commande', None)

    if id_commande is not None:
        sql_telephones = '''SELECT ligne_commande.*, telephone.nom_telephone AS nom, 
                 (ligne_commande.prix * ligne_commande.quantite) AS prix_ligne,
                 commande.id_commande AS commande_id,
                 commande.etat_id AS etat_id  
                 FROM ligne_commande
                 JOIN telephone ON ligne_commande.telephone_id = telephone.id_telephone
                 JOIN commande ON ligne_commande.commande_id = commande.id_commande
                 WHERE ligne_commande.commande_id = %s'''
        mycursor.execute(sql_telephones, (id_commande,))
        telephones_commande = mycursor.fetchall()

        sql_adresse_livraison = '''SELECT adresse.rue AS rue_livraison, 
                                   adresse.code_postal AS code_postal_livraison, 
                                   adresse.ville AS ville_livraison
                                   FROM commande
                                   JOIN adresse ON commande.adresse_livraison_id = adresse.id_adresse
                                   WHERE commande.id_commande = %s'''
        mycursor.execute(sql_adresse_livraison, (id_commande,))
        adresse_livraison = mycursor.fetchone()

        sql_adresse_facturation = '''SELECT adresse.rue AS rue_facturation, 
                                     adresse.code_postal AS code_postal_facturation, 
                                     adresse.ville AS ville_facturation
                                     FROM commande
                                     JOIN adresse ON commande.adresse_facturation_id = adresse.id_adresse
                                     WHERE commande.id_commande = %s'''
        mycursor.execute(sql_adresse_facturation, (id_commande,))
        adresse_facturation = mycursor.fetchone()

        commande_adresses = {}
        if adresse_livraison:
            commande_adresses.update({
                'rue_livraison': adresse_livraison['rue_livraison'],
                'code_postal_livraison': adresse_livraison['code_postal_livraison'],
                'ville_livraison': adresse_livraison['ville_livraison']
            })
        if adresse_facturation:
            commande_adresses.update({
                'rue_facturation': adresse_facturation['rue_facturation'],
                'code_postal_facturation': adresse_facturation['code_postal_facturation'],
                'ville_facturation': adresse_facturation['ville_facturation']
            })

    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , telephones_commande=telephones_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get', 'post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id is not None:
        # Mise à jour de l'état de la commande vers "expédié" (id_etat=2)
        sql = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s'''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
        flash(u'Commande validée et expédiée', 'alert-success')
    return redirect('/admin/commande/show')