#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/telephone/commentaires', methods=['GET'])
def admin_telephone_details():
    mycursor = get_db().cursor()
    id_telephone =  request.args.get('id_telephone', None)
    id_utilisateur = request.args.get('id_utilisateur', None)
    sql = ''' SELECT commentaire.texte AS commentaire, commentaire.date_publication, utilisateur.nom AS nom, 
     commentaire.utilisateur_id AS id_utilisateur, commentaire.telephone_id As id_telephone, commentaire.valider AS valider
     FROM commentaire
     JOIN utilisateur ON commentaire.utilisateur_id = utilisateur.id_utilisateur
     WHERE commentaire.telephone_id = %s
     ORDER BY commentaire.date_publication DESC, commentaire.valider ASC;'''
    mycursor.execute(sql, (id_telephone,))
    commentaires = mycursor.fetchall()

    sql = ''' SELECT telephone.nom_telephone, COUNT(note) AS nb_notes, AVG(note) AS moyenne_notes, telephone.id_telephone
     FROM telephone
     LEFT JOIN note ON telephone.id_telephone = note.telephone_id
     LEFT JOIN commentaire ON telephone.id_telephone = commentaire.telephone_id
     WHERE id_telephone = %s 
     GROUP BY telephone.nom_telephone, telephone.id_telephone;'''
    mycursor.execute(sql, (id_telephone,))
    telephone = mycursor.fetchone()

    sql = ''' 
    SELECT
        (SELECT COUNT(*) FROM commentaire WHERE telephone_id = %s) AS nb_commentaires_total,
        (SELECT COUNT(*) FROM commentaire WHERE telephone_id = %s AND valider = 1) AS nb_commentaires_valider'''
    mycursor.execute(sql, (id_telephone, id_telephone))
    nb_commentaires = mycursor.fetchone()

    return render_template('admin/telephone/show_telephone_commentaires.html'
                           , commentaires=commentaires
                           , telephone=telephone
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/telephone/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_telephone = request.form.get('id_telephone', None)
    date_publication = request.form.get('date_publication', None)
    sql = ''' DELETE FROM commentaire WHERE utilisateur_id = %s AND telephone_id = %s AND date_publication = %s; '''
    tuple_delete=(id_utilisateur,id_telephone,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/admin/telephone/commentaires?id_telephone='+id_telephone)


@admin_commentaire.route('/admin/telephone/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_telephone = request.args.get('id_telephone', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/telephone/add_commentaire.html',id_utilisateur=id_utilisateur,id_telephone=id_telephone,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_telephone = request.form.get('id_telephone', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    tuple_insert = (commentaire, id_utilisateur, id_telephone)
    sql = ''' INSERT INTO commentaire(texte, utilisateur_id, telephone_id, date_publication, valider) 
    VALUES (%s, %s, %s, current_timestamp, 1); '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/admin/telephone/commentaires?id_telephone='+id_telephone)


@admin_commentaire.route('/admin/telephone/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_telephone = request.args.get('id_telephone', None)
    mycursor = get_db().cursor()
    sql = ''' UPDATE commentaire SET valider = 1 WHERE telephone_id = %s '''
    mycursor.execute(sql, (id_telephone,))
    get_db().commit()
    return redirect('/admin/telephone/commentaires?id_telephone='+id_telephone)