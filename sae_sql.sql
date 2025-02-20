-- Suppression des tables si elles existent
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS telephone;
DROP TABLE IF EXISTS type_telephone;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS historique;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS declinaison_telephone;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS etat;

-- Création des tables principales
CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(50),
    email VARCHAR(250),
    nom VARCHAR(250),
    password VARCHAR(250),
    role VARCHAR(250),
    est_actif TINYINT(1),
    PRIMARY KEY(id_utilisateur)
);

CREATE TABLE adresse (
    id_adresse INT AUTO_INCREMENT,
    nom VARCHAR(255),
    code_postal VARCHAR(10),
    ville VARCHAR(100),
    id_utilisateur INT,
    date_utilisation DATETIME,  -- Ajout de date_utilisation
    PRIMARY KEY(id_adresse),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATETIME,
    id_adresse INT,
    id_utilisateur INT,
    id_etat INT,  -- Ajout de la clé étrangère id_etat
    PRIMARY KEY(id_commande),
    FOREIGN KEY (id_adresse) REFERENCES adresse(id_adresse),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_etat) REFERENCES etat(id_etat)
);

CREATE TABLE couleur (
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(50) NOT NULL,
    code_couleur VARCHAR(10) NOT NULL,  -- Ajout de code_couleur
    PRIMARY KEY(id_couleur),
    UNIQUE(libelle_couleur)
);

CREATE TABLE type_telephone (
    id_type_telephone INT AUTO_INCREMENT,
    libelle_type_telephone VARCHAR(50) NOT NULL,
    PRIMARY KEY(id_type_telephone),
    UNIQUE(libelle_type_telephone)
);

CREATE TABLE telephone (
    id_telephone INT AUTO_INCREMENT,
    nom_telephone VARCHAR(50) NOT NULL,
    poids INT,
    taille DECIMAL(2,1),
    prix_telephone DECIMAL(15,2),
    couleur_id INT,
    fournisseur VARCHAR(50) NOT NULL,
    marque VARCHAR(50) NOT NULL,
    type_telephone_id INT,
    stock INT,
    image VARCHAR(50),
    PRIMARY KEY(id_telephone),
    FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur),
    FOREIGN KEY (type_telephone_id) REFERENCES type_telephone(id_type_telephone)
);


CREATE TABLE ligne_commande (
    id_commande INT,
    id_telephone INT,
    quantite INT,
    prix_unitaire DECIMAL(15,2),
    FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
    FOREIGN KEY (id_telephone) REFERENCES telephone(id_telephone)
);

CREATE TABLE declinaison_telephone (
    id_telephone INT,
    id_couleur INT,
    FOREIGN KEY (id_telephone) REFERENCES telephone(id_telephone),
    FOREIGN KEY (id_couleur) REFERENCES couleur(id_couleur)
);

CREATE TABLE historique (
    id_utilisateur INT,
    id_telephone INT,
    date_consultation DATETIME,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_telephone) REFERENCES telephone(id_telephone)
);

CREATE TABLE note (
    id_utilisateur INT,
    id_telephone INT,
    note INT CHECK (note BETWEEN 1 AND 5),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_telephone) REFERENCES telephone(id_telephone)
);

CREATE TABLE commentaire (
    id_utilisateur INT,
    id_telephone INT,
    texte TEXT,
    date_publication DATETIME,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_telephone) REFERENCES telephone(id_telephone)
);

CREATE TABLE etat (
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(50) NOT NULL,
    PRIMARY KEY(id_etat)
);


INSERT INTO telephone (nom_telephone, poids, taille, prix_telephone, couleur_id, fournisseur, marque, type_telephone_id, stock, image) VALUES
    ('iPhone 13 128Go', 174, 6.1, 909.00, 10, 'Apple Store', 'Apple', 2, 45, 'iphone13blanc.jpg'),
    ('iPhone 13 256Go', 174, 6.1, 1029.00, 2, 'Apple Store', 'Apple', 1, 32, 'iphone13bleu.jpg'),
    ('iPhone 13 Pro 256Go', 204, 6.1, 1259.00, 9, 'Apple Store', 'Apple', 1, 28, 'iphone13provert.jpg'),
    ('iPhone 13 Mini 128Go', 140, 5.4, 809.00, 1, 'Apple Store', 'Apple', 2, 15, 'iphone13mininoir.jpg'),
    ('iPhone 14 128Go', 172, 6.1, 1019.00, 6, 'Apple Store', 'Apple', 1, 52, 'iphone14jaune.jpg'),
    ('iPhone 14 256Go', 172, 6.7, 1199.00, 4, 'Apple Store', 'Apple', 1, 38, 'iphone14rouge.jpg'),
    ('iPhone 14 Pro 512Go', 206, 6.1, 1529.00, 11, 'Apple Store', 'Apple', 1, 25, 'iphone14proviolet.jpg'),
    ('iPhone 14 Pro Max 1To', 240, 6.7, 1829.00, 5, 'Apple Store', 'Apple', 1, 12, 'iphone14promaxgold.jpg'),
    ('iPhone 15 128Go', 171, 6.1, 1099.00, 7, 'Apple Store', 'Apple', 1, 65, 'iphone15rose.jpg'),
    ('iPhone 15 Plus 256Go', 201, 6.7, 1299.00, 2, 'Apple Store', 'Apple', 1, 42, 'iphone15plusbleu.jpg'),
    ('iPhone 15 Pro 256Go', 191, 6.1, 1449.00, 1, 'Apple Store', 'Apple', 1, 35, 'iphone15pronoir.jpg'),
    ('iPhone 15 256Go', 221, 6.7, 1669.00, 6, 'Apple Store', 'Apple', 1, 28, 'iphone15jaune.jpg'),
    ('iPhone 16 256Go', 175, 6.1, 1199.00, 10, 'Apple Store', 'Apple', 1, 75, 'iphone16blanc.jpg'),
    ('iPhone 16 Pro 256Go', 190, 6.1, 1499.00, 1, 'Apple Store', 'Apple', 1, 48, 'iphone16pro.jpg'),
    ('iPhone 16 Pro Max 1To', 220, 6.7, 1799.00, 8, 'Apple Store', 'Apple', 1, 22, 'iphone16promaxtitan.jpg'),
    ('iPhone 16 Pro 512Go', 195, 6.1, 1649.00, 3, 'Apple Store', 'Apple', 1, 31, 'iphone16proargent.jpg'),
    ('iPhone 16 Pro Max 256Go', 225, 6.7, 1649.00, 1, 'Apple Store', 'Apple', 1, 40, 'iphone16promaxnoir.jpg');

INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom, est_actif) VALUES
    (1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
    (2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
    (3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');











