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

    sql = "SELECT * FROM ligne_panier telephone_id=%s AND utilisateur_id=%s"
    mycursor.execute(sql, (id_telephone, id_client))
    telephone_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM telephone WHERE id_telephone=%s", (id_telephone))
    telephone = mycursor.fetchone()

    if not (telephone_panier is None) and telephone_panier['quantite'] >= 1:
        tuple_update = (quantite, id_client, id_telephone)
        sql = "UPDATE ligne_panier SET quantite = quantite+%s WHERE utilisateur_id=%s AND telephone_id=%s"
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (id_client, id_telephone, quantite)
        sql = "INSERT INTO ligne_panier(utilisateur_id,telephone_id,quantite,date_ajout) VALUES (%s, %s, %s, current_timestamp)"
        mycursor.execute(sql, tuple_insert)

    get_db().commit()

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


    return redirect('/client/telephone/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'telephone
    # id_declinaison_telephone = request.form.get('id_declinaison_telephone', None)

    sql = ''' selection de la ligne du panier pour l'telephone et l'utilisateur connecté'''
    telephone_panier=[]

    if not(telephone_panier is None) and telephone_panier['quantite'] > 1:
        sql = ''' mise à jour de la quantité dans le panier => -1 telephone '''
    else:
        sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'telephone disponible
    get_db().commit()
    return redirect('/client/telephone/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'telephone pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'telephone : stock = stock + qté de la ligne pour l'telephone'''
        get_db().commit()
    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_telephone = request.form.get('id_declinaison_telephone')

    sql = ''' selection de ligne du panier '''

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
    # mise en session des variables
    return redirect('/client/telephone/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/telephone/show')
