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

    # ---------
    #id_declinaison_telephone=request.form.get('id_declinaison_telephone',None)
    id_declinaison_telephone = 1

# ajout dans le panier d'une déclinaison d'un telephone (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_telephone))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_telephone = declinaisons[0]['id_declinaison_telephone']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_telephone))
    #     telephone = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_telephone.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , telephone=telephone)

# ajout dans le panier d'un telephone

    sql = "SELECT * FROM ligne_panier WHERE telephone_id=%s AND utilisateur_id=%s"
    mycursor.execute(sql, (id_telephone, id_client))
    telephone_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM telephone WHERE id_telephone=%s", (id_telephone))
    telephone = mycursor.fetchone()

    mycursor.execute("SELECT stock FROM telephone WHERE id_telephone=%s", (id_telephone))
    telephone_stock = mycursor.fetchone()

    if telephone_stock is not None and 'stock' in telephone_stock and telephone_stock['stock'] >=  int(quantite):
        tuple_update = (quantite, id_telephone)
        sql = "UPDATE telephone SET stock=stock-%s WHERE id_telephone=%s;"
        mycursor.execute(sql, tuple_update)

        if not (telephone_panier is None) and telephone_panier['quantite'] >= 1:
            tuple_update = (quantite, id_client, id_telephone)
            sql = "UPDATE ligne_panier SET quantite = quantite+%s WHERE utilisateur_id=%s AND telephone_id=%s"
            mycursor.execute(sql, tuple_update)
        else:
            tuple_insert = (id_client, id_telephone, quantite)
            sql = "INSERT INTO ligne_panier(utilisateur_id,telephone_id,quantite,date_ajout) VALUES (%s, %s, %s, current_timestamp)"
            mycursor.execute(sql, tuple_insert)
    else:
        flash(u'Stock insuffisant')

    get_db().commit()

    return redirect('/client/telephone/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone','')
    quantite = 1
    print('supprime client : ', id_client, 'telephone : ', id_telephone, 'quantite : ', quantite)
    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s"
    mycursor.execute(sql, (id_client, id_telephone))
    telephone_panier = mycursor.fetchone()

    if not(telephone_panier is None) and telephone_panier['quantite'] > 1:
        sql = "UPDATE ligne_panier SET quantite = quantite-%s WHERE utilisateur_id=%s AND telephone_id=%s"
        mycursor.execute(sql, (quantite, id_client, id_telephone))
    else:
        sql = "DELETE FROM ligne_panier WHERE utilisateur_id=%s AND telephone_id=%s"
        mycursor.execute(sql, (id_client, id_telephone))

    # ---------
    # partie 2 : on supprime une déclinaison du telephone
    # id_declinaison_telephone = request.form.get('id_declinaison_telephone', None)

    # mise à jour du stock du telephone disponible
    sql = "UPDATE telephone SET stock = stock + %s WHERE id_telephone = %s"
    mycursor.execute(sql, (quantite, id_telephone))

    get_db().commit()
    return redirect('/client/telephone/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'telephone pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'telephone : stock = stock + qté de la ligne pour l'telephone'''
        get_db().commit()
    id_client = session['id_user']
    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s"
    retour = mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = "DELETE FROM ligne_panier WHERE telephone_id=%s AND utilisateur_id=%s"
        mycursor.execute(sql, (item['telephone_id'], id_client))
        #remettre les articles en stock
        sql2 = "UPDATE telephone SET stock = stock + %s WHERE id_telephone = %s"
        mycursor.execute(sql2, (item['quantite'], item['telephone_id']))
        get_db().commit()
    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_telephone = request.form.get('id_declinaison_telephone')

    sql = "SELECT * FROM ligne_panier WHERE utilisateur_id=%s"

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'telephone : stock = stock + qté de la ligne pour l'telephone'''

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
