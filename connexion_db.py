from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host="localhost",
            # host="localhost",
            user="sae_s2_03_04_05",
            password="mdp",
            database="BDD_SAE_S2_03_04_05",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        # à activer sur les machines personnelles :
        activate_db_options(db)
    return db

def activate_db_options(db):
    cursor = db.cursor()
    # Vérifier et activer l'option ONLY_FULL_GROUP_BY si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            print('MYSQL : il manque le mode ONLY_FULL_GROUP_BY')  # mettre en commentaire
            cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
            db.commit()
        else:
            print('MYSQL : mode ONLY_FULL_GROUP_BY ok')  # mettre en commentaire
    # Vérifier et activer l'option lower_case_table_names si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result:
        if result['Value'] != '0':
            print('MYSQL : valeur de la variable globale lower_case_table_names differente de 0')  # mettre en commentaire
            cursor.execute("SET GLOBAL lower_case_table_names = 0")
            db.commit()
        else:
            print('MYSQL : variable globale lower_case_table_names=0 ok')  # mettre en commentaire
    cursor.close()

def get_filtered_products():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM telephone WHERE 1=1"
    params = []
    if session.get("filter_word"):
        query += " AND (marque LIKE %s OR modele LIKE %s)"
        params.extend([f"%{session['filter_word']}%", f"%{session['filter_word']}%"])
    if session.get("filter_prix_min"):
        query += " AND prix >= %s"
        params.append(session["filter_prix_min"])
    if session.get("filter_prix_max"):
        query += " AND prix <= %s"
        params.append(session["filter_prix_max"])
    if session.get("filter_types"):
        placeholders = ",".join(["%s"] * len(session["filter_types"]))
        query += f" AND id_type_telephone IN ({placeholders})"
        params.extend(session["filter_types"])
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    return results