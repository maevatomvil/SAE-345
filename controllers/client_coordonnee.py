#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = "SELECT login, nom, email FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, id_client)
    utilisateur=mycursor.fetchone()

    sql = '''SELECT adresse.id_adresse, adresse.nom, adresse.rue, adresse.ville, adresse.code_postal, COUNT(commande.adresse_livraison_id) as nbr_commandes, adresse.valide, adresse.favori
             FROM adresse 
             LEFT JOIN commande ON adresse.id_adresse = commande.adresse_livraison_id
             WHERE adresse.utilisateur_id = %s
             GROUP BY adresse.id_adresse, adresse.nom, adresse.rue, adresse.ville, adresse.code_postal, adresse.valide, adresse.favori'''
    mycursor.execute(sql, id_client)
    adresses=mycursor.fetchall()
    print(adresses)

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                         #  , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = "SELECT login, nom, email FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, id_client)
    utilisateur=mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    sql = "SELECT email, login FROM utilisateur WHERE email=%s OR login=%s"
    mycursor.execute(sql, (email, login))

    utilisateur=mycursor.fetchall()
    if utilisateur:
        flash(u'cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        sql = "SELECT login, nom, email FROM utilisateur WHERE id_utilisateur = %s"
        mycursor.execute(sql, id_client)
        utilisateur=mycursor.fetchone()
        return render_template('client/coordonnee/edit_coordonnee.html'
                               , utilisateur=utilisateur
                               )
    
    sql = "UPDATE utilisateur SET login = %s, email = %s, nom = %s WHERE id_utilisateur = %s"
    mycursor.execute(sql, (login, email, nom, id_client))


    get_db().commit()
    flash(u'Profil modifié avec succès', 'alert-success')
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    sql = "SELECT * FROM commande WHERE adresse_livraison_id = %s OR adresse_facturation_id = %s"
    mycursor.execute(sql, (id_adresse, id_adresse))
    adresses=mycursor.fetchall()


    if adresses:
        sql = "UPDATE adresse SET favori = 0, valide = 0 WHERE id_adresse = %s"
        mycursor.execute(sql, id_adresse)
        get_db().commit()
        flash(u'Addresse supprimée avec succès', 'alert-danger')

        return redirect('/client/coordonnee/show')

    sql = "DELETE FROM adresse WHERE id_adresse = %s"
    mycursor.execute(sql, (id_adresse))
    get_db().commit()
    flash(u'Addresse supprimée avec succès', 'alert-danger')

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = "SELECT login, nom, email FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, id_client)
    utilisateur=mycursor.fetchone()

    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    pays = request.form.get('pays')
    sql = "UPDATE adresse SET favori = 0 WHERE utilisateur_id = %s"
    mycursor.execute(sql, id_client)
    get_db().commit()

    sql = "INSERT INTO adresse(utilisateur_id, nom, rue, ville, code_postal, pays, valide, favori) VALUES (%s, %s, %s, %s, %s, %s, 1, 1)"
    mycursor.execute(sql, (id_client, nom, rue, ville, code_postal, pays))
    get_db().commit()
    flash(u'Addresse ajoutée avec succès', 'alert-success')
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    sql = "SELECT login, nom, email FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, id_client)
    utilisateur=mycursor.fetchone()

    sql = "SELECT * FROM adresse WHERE adresse.id_adresse = %s"
    mycursor.execute(sql, id_adresse)
    adresse=mycursor.fetchone()
    print(adresse)

    return render_template('/client/coordonnee/edit_adresse.html'
                           ,utilisateur=utilisateur
                           ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    pays = request.form.get('pays')
    id_adresse = request.form.get('id_adresse')

    sql = "UPDATE adresse SET favori = 0 WHERE utilisateur_id = %s"
    mycursor.execute(sql, id_client)
    get_db().commit()

    sql = "SELECT * FROM commande WHERE adresse_livraison_id = %s OR adresse_facturation_id = %s"
    mycursor.execute(sql, (id_adresse, id_adresse))
    adresses=mycursor.fetchall()

    if adresses:
        sql = "UPDATE adresse SET valide = 0 WHERE id_adresse = %s"
        mycursor.execute(sql, id_adresse)
        get_db().commit()

        sql = "INSERT INTO adresse(utilisateur_id, nom, rue, ville, code_postal, pays, valide, favori) VALUES (%s, %s, %s, %s, %s, %s, 1, 1)"
        mycursor.execute(sql, (id_client, nom, rue, ville, code_postal, pays))
        get_db().commit()
        flash(u'Addresse modifiée avec succès', 'alert-success')

        return redirect('/client/coordonnee/show')

    sql = "UPDATE adresse SET nom = %s, rue = %s, code_postal = %s, ville = %s, pays = %s, favori = 1 WHERE id_adresse = %s"
    mycursor.execute(sql, (nom, rue, code_postal, ville, pays, id_adresse))
    get_db().commit()
    flash(u'Addresse modifiée avec succès', 'alert-success')

    return redirect('/client/coordonnee/show')
