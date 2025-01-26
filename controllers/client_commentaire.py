#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/telephone/details', methods=['GET'])
def client_telephone_details():
    mycursor = get_db().cursor()
    id_telephone =  request.args.get('id_telephone', None)
    id_client = session['id_user']

    ## partie 4
    # client_historique_add(id_telephone, id_client)

    sql = '''   
       SELECT id_telephone
               , nom_telephone AS nom
               , prix_telephone AS prix
               , poids
               , taille
               , libelle_couleur AS couleur
               , libelle_type_telephone AS type
        FROM telephone
        JOIN couleur ON telephone.couleur_id = couleur.id_couleur
        JOIN type_telephone ON telephone.type_telephone_id = type_telephone.id_type_telephone
        WHERE id_telephone = %s;'''
    #mycursor.execute(sql, id_telephone)
    #telephone = mycursor.fetchone()
    telephone=[]
    commandes_telephones=[]
    nb_commentaires=[]
    if telephone is None:
        abort(404, "pb id telephone")
    # sql = ''''''
    # mycursor.execute(sql, (id_telephone))
    # commentaires = mycursor.fetchall()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_telephone))
    # commandes_telephones = mycursor.fetchone()
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_telephone))
    # note = mycursor.fetchone()
    # print('note',note)
    # if note:
    #     note=note['note']
    # sql = '''
    # '''
    # mycursor.execute(sql, (id_client, id_telephone))
    # nb_commentaires = mycursor.fetchone()
    return render_template('client/telephone_info/telephone_details.html'
                           , telephone=telephone
                           # , commentaires=commentaires
                           , commandes_telephones=commandes_telephones
                           # , note=note
                            , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/telephone/details?id_telephone='+id_telephone)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/telephone/details?id_telephone='+id_telephone)

    tuple_insert = (commentaire, id_client, id_telephone)
    print(tuple_insert)
    sql = '''  '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/telephone/details?id_telephone='+id_telephone)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''   '''
    tuple_delete=(id_client,id_telephone,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/telephone/details?id_telephone='+id_telephone)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_telephone = request.form.get('id_telephone', None)
    tuple_insert = (note, id_client, id_telephone)
    print(tuple_insert)
    sql = '''   '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/telephone/details?id_telephone='+id_telephone)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_telephone = request.form.get('id_telephone', None)
    tuple_update = (note, id_client, id_telephone)
    print(tuple_update)
    sql = '''  '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/telephone/details?id_telephone='+id_telephone)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_telephone = request.form.get('id_telephone', None)
    tuple_delete = (id_client, id_telephone)
    print(tuple_delete)
    sql = '''  '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/telephone/details?id_telephone='+id_telephone)
