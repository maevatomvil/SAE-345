#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_telephone = Blueprint('admin_telephone', __name__,
                          template_folder='templates')


@admin_telephone.route('/admin/telephone/show')
def show_telephone():
    mycursor = get_db().cursor()

    filter_stock = request.args.get('filter_stock')

    sql = '''
    SELECT 
        telephone.id_telephone, 
        telephone.nom_telephone as nom, 
        telephone.type_telephone_id, 
        telephone.prix_telephone as prix,
        COALESCE(telephone.poids, 'N/A') as poids,
        COALESCE(telephone.taille, 'N/A') as taille,
        COALESCE(telephone.fournisseur, 'N/A') as fournisseur,
        COALESCE(telephone.marque, 'N/A') as marque,
        telephone.stock, 
        telephone.image, 
        type_telephone.libelle_type_telephone as libelle
    FROM telephone
    LEFT JOIN type_telephone ON telephone.type_telephone_id = type_telephone.id_type_telephone
    '''

    params = []
    if filter_stock == 'low':
        sql += ' WHERE telephone.stock <= 5 AND telephone.stock > 0'
    elif filter_stock == 'out':
        sql += ' WHERE telephone.stock = 0'

    sql += ' ORDER BY telephone.nom_telephone'

    mycursor.execute(sql, params)
    telephones = mycursor.fetchall()

    return render_template('admin/telephone/show_telephone.html',
                           telephones=telephones,
                           filter_stock=filter_stock)


@admin_telephone.route('/admin/telephone/add', methods=['GET'])
def add_telephone():
    mycursor = get_db().cursor()

    sql = '''SELECT id_type_telephone, libelle_type_telephone as libelle 
             FROM type_telephone 
             ORDER BY libelle_type_telephone'''
    mycursor.execute(sql)
    types_telephone = mycursor.fetchall()

    return render_template('admin/telephone/add_telephone.html',
                           types_telephone=types_telephone)


@admin_telephone.route('/admin/telephone/add', methods=['POST'])
def valid_add_telephone():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_telephone_id = request.form.get('type_telephone_id', '')
    prix = request.form.get('prix', '')
    fournisseur = request.form.get('fournisseur', '')
    marque = request.form.get('marque', '')
    poids = request.form.get('poids', None)
    taille = request.form.get('taille', None)
    stock = request.form.get('stock', 0)
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        filename = None

    sql = '''INSERT INTO telephone(
                nom_telephone, 
                image, 
                prix_telephone, 
                type_telephone_id, 
                fournisseur, 
                marque, 
                poids, 
                taille, 
                stock
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    tuple_add = (
        nom,
        filename,
        prix,
        type_telephone_id,
        fournisseur,
        marque,
        poids,
        taille,
        stock
    )

    mycursor.execute(sql, tuple_add)
    get_db().commit()

    message = f'Téléphone ajouté : {nom} - Type: {type_telephone_id} - Prix: {prix} - Fournisseur: {fournisseur} - Marque: {marque}'
    flash(message, 'alert-success')

    return redirect('/admin/telephone/show')



@admin_telephone.route('/admin/telephone/delete', methods=['GET'])
def delete_telephone():
    id_telephone = request.args.get('id_telephone')
    mycursor = get_db().cursor()

    sql = '''SELECT COUNT(*) AS nb_commandes FROM ligne_commande WHERE telephone_id = %s'''
    mycursor.execute(sql, (id_telephone,))
    result = mycursor.fetchone()
    nb_commandes = result['nb_commandes'] if result else 0

    sql = '''SELECT COUNT(*) AS nb_commentaires FROM commentaire WHERE telephone_id = %s'''
    mycursor.execute(sql, (id_telephone,))
    result = mycursor.fetchone()
    nb_commentaires = result['nb_commentaires'] if result else 0

    if nb_commandes > 0:
        message = u'Impossible de supprimer ce téléphone : il est présent dans ' + str(nb_commandes) + ' commande(s)'
        flash(message, 'alert-warning')
    elif nb_commentaires > 0:
        message = u'Impossible de supprimer ce téléphone : il a ' + str(nb_commentaires) + ' commentaire(s) associé(s)'
        flash(message, 'alert-warning')
    else:
        sql = '''SELECT COUNT(*) AS nb_panier FROM ligne_panier WHERE telephone_id = %s'''
        mycursor.execute(sql, (id_telephone,))
        result = mycursor.fetchone()
        nb_panier = result['nb_panier'] if result else 0

        if nb_panier > 0:
            message = u'Impossible de supprimer ce téléphone : il est présent dans ' + str(nb_panier) + ' panier(s)'
            flash(message, 'alert-warning')
        else:
            sql = '''SELECT * FROM telephone WHERE id_telephone = %s'''
            mycursor.execute(sql, (id_telephone,))
            telephone = mycursor.fetchone()

            if telephone:
                image = telephone['image']

                sql = '''DELETE FROM telephone WHERE id_telephone = %s'''
                mycursor.execute(sql, (id_telephone,))
                get_db().commit()

                #if image is not None:
                    #image_path = os.path.join('static/images/', image)
                    #if os.path.exists(image_path):
                        #os.remove(image_path)

                print("un telephone supprimé, id :", id_telephone)
                message = u'un telephone supprimé, id : ' + id_telephone
                flash(message, 'alert-success')
            else:
                message = u'Téléphone non trouvé avec l\'id : ' + id_telephone
                flash(message, 'alert-warning')

    return redirect('/admin/telephone/show')


@admin_telephone.route('/admin/telephone/edit', methods=['GET'])
def edit_telephone():
    id_telephone = request.args.get('id_telephone')
    mycursor = get_db().cursor()

    # Updated SQL to fetch all new columns
    sql = '''
    SELECT 
        telephone.id_telephone, 
        telephone.nom_telephone as nom, 
        telephone.prix_telephone as prix, 
        telephone.type_telephone_id, 
        telephone.image, 
        telephone.stock,
        telephone.poids,
        telephone.taille,
        telephone.fournisseur,
        telephone.marque,
        type_telephone.libelle_type_telephone as libelle
    FROM telephone
    LEFT JOIN type_telephone ON telephone.type_telephone_id = type_telephone.id_type_telephone
    WHERE telephone.id_telephone = %s
    '''
    mycursor.execute(sql, (id_telephone,))
    telephone = mycursor.fetchone()

    # Fetch types of telephones
    sql = '''
    SELECT id_type_telephone, libelle_type_telephone as libelle
    FROM type_telephone
    ORDER BY libelle_type_telephone
    '''
    mycursor.execute(sql)
    types_telephone = mycursor.fetchall()

    return render_template('admin/telephone/edit_telephone.html',
                           telephone=telephone,
                           types_telephone=types_telephone)


@admin_telephone.route('/admin/telephone/edit', methods=['POST'])
def valid_edit_telephone():
    mycursor = get_db().cursor()

    # Collect form data
    id_telephone = request.form.get('id_telephone')
    nom = request.form.get('nom')
    type_telephone_id = request.form.get('type_telephone_id')
    prix = request.form.get('prix')
    fournisseur = request.form.get('fournisseur')
    marque = request.form.get('marque')
    poids = request.form.get('poids', None)
    taille = request.form.get('taille', None)
    stock = request.form.get('stock')
    image = request.files.get('image', '')

    # Fetch existing image name
    sql = '''SELECT image FROM telephone WHERE id_telephone = %s'''
    mycursor.execute(sql, (id_telephone,))
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']

    # Handle image upload
    if image:
        # Remove old image if exists
        if image_nom and image_nom != "" and os.path.exists(os.path.join(os.getcwd(), "static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd(), "static/images/", image_nom))

        # Generate unique filename
        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
        image_nom = filename

    # Update SQL
    sql = '''
    UPDATE telephone 
    SET 
        nom_telephone = %s, 
        image = %s, 
        prix_telephone = %s, 
        type_telephone_id = %s,
        fournisseur = %s,
        marque = %s,
        poids = %s,
        taille = %s,
        stock = %s
    WHERE id_telephone = %s
    '''

    mycursor.execute(sql, (
        nom,
        image_nom,
        prix,
        type_telephone_id,
        fournisseur,
        marque,
        poids,
        taille,
        stock,
        id_telephone
    ))

    get_db().commit()

    # Prepare flash message
    message = f'Téléphone modifié : {nom} - Type: {type_telephone_id} - Prix: {prix}'
    flash(message, 'alert-success')

    return redirect('/admin/telephone/show')







@admin_telephone.route('/admin/telephone/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    telephone=[]
    commentaires = {}
    return render_template('admin/telephone/show_avis.html'
                           , telephone=telephone
                           , commentaires=commentaires
                           )


@admin_telephone.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    telephone_id = request.form.get('idtelephone', None)
    userId = request.form.get('idUser', None)

    return admin_avis(telephone_id)
