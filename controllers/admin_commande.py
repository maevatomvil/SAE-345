#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
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

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = '''SELECT ligne_commande.*, telephone.nom_telephone AS nom, 
                 (ligne_commande.prix * ligne_commande.quantite) AS prix_ligne  
                 FROM ligne_commande
                 JOIN telephone ON ligne_commande.telephone_id = telephone.id_telephone
                 WHERE ligne_commande.commande_id = %s'''
        mycursor.execute(sql, id_commande)
        articles_commande = mycursor.fetchall()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )