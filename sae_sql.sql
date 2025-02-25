DROP TABLE IF EXISTS liste_envie;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS historique;
DROP TABLE IF EXISTS paiement;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS telephone;
DROP TABLE IF EXISTS type_telephone;
DROP TABLE IF EXISTS couleur;


CREATE TABLE couleur (
    id_couleur INT AUTO_INCREMENT,
    libelle_couleur VARCHAR(50) NOT NULL,
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
    couleur_id INT,
    prix_telephone DECIMAL(15,2),
    fournisseur VARCHAR(50) NOT NULL,
    marque VARCHAR(50) NOT NULL,
    type_telephone_id INT,
    stock INT,
    image VARCHAR(50),
    PRIMARY KEY(id_telephone),
    FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur),
    FOREIGN KEY (type_telephone_id) REFERENCES type_telephone(id_type_telephone)
);

CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(50),
    email VARCHAR(250),
    nom VARCHAR(250),
    password VARCHAR(250),
    role VARCHAR(250),
    est_actif tinyint(1),
    PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat (
    id_etat int(11) NOT NULL AUTO_INCREMENT,
    libelle varchar(255),
    PRIMARY KEY (id_etat)
);

CREATE TABLE ligne_panier (
    utilisateur_id INT,
    telephone_id INT,
    date_ajout DATETIME,
    quantite INT,
    PRIMARY KEY (utilisateur_id, telephone_id, date_ajout),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
);

CREATE TABLE adresse (
    id_adresse INT AUTO_INCREMENT,
    utilisateur_id INT,
    rue VARCHAR(255),
    ville VARCHAR(100),
    code_postal VARCHAR(20),
    pays VARCHAR(100),
    type_adresse VARCHAR(50),
    PRIMARY KEY (id_adresse),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATETIME,
    etat_id INT NOT NULL,
    utilisateur_id INT NOT NULL,
    adresse_livraison_id INT,
    adresse_facturation_id INT,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (adresse_livraison_id) REFERENCES adresse(id_adresse),
    FOREIGN KEY (adresse_facturation_id) REFERENCES adresse(id_adresse)
);

CREATE TABLE ligne_commande (
    commande_id int(11),
    telephone_id int(11),
    prix decimal(15,2),
    quantite int(11),
    PRIMARY KEY (commande_id, telephone_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
);

CREATE TABLE paiement (
    id_paiement INT AUTO_INCREMENT,
    commande_id INT,
    montant DECIMAL(15,2),
    date_paiement DATETIME,
    methode VARCHAR(50),
    statut VARCHAR(50),
    PRIMARY KEY (id_paiement),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande)
);

CREATE TABLE historique (
    utilisateur_id INT,
    telephone_id INT,
    date_consultation DATETIME,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
);

CREATE TABLE note (
    utilisateur_id INT,
    telephone_id INT,
    note INT CHECK (note BETWEEN 1 AND 5),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
);

CREATE TABLE commentaire (
    utilisateur_id INT,
    telephone_id INT,
    texte TEXT,
    date_publication DATETIME,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
);

CREATE TABLE liste_envie(
    utilisateur_id INT,
    telephone_id INT,
    date_consultation DATETIME,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone)
);

INSERT INTO couleur (libelle_couleur) VALUES
    ('Noir'),
    ('Bleu'),
    ('Argent'),
    ('Rouge'),
    ('Or'),
    ('Jaune'),
    ('Rose'),
    ('Titane'),
    ('Vert'),
    ('Blanc'),
    ('Violet');

INSERT INTO type_telephone(libelle_type_telephone) VALUES
    ('Smartphone'),
    ('Clapet'),
    ('Touches'),
    ('Fixe');

INSERT INTO telephone (nom_telephone, poids, taille, couleur_id, prix_telephone, fournisseur, marque, type_telephone_id, stock, image) VALUES
    ('iPhone 13 128Go', 174, 6.1, 10, 909.00, 'Apple Store', 'Apple', 1, 45, 'iphone13blanc.jpg'),
    ('iPhone 13 256Go', 174, 6.1, 2, 1029.00, 'Apple Store', 'Apple', 1, 32, 'iphone13bleu.jpg'),
    ('iPhone 13 Pro 256Go', 204, 6.1, 9, 1259.00, 'Apple Store', 'Apple', 1, 28, 'iphone13provert.jpg'),
    ('iPhone 13 Mini 128Go', 140, 5.4, 1, 809.00, 'Apple Store', 'Apple', 1, 15, 'iphone13mininoir.jpg'),
    ('iPhone 14 128Go', 172, 6.1, 6, 1019.00, 'Apple Store', 'Apple', 1, 52, 'iphone14jaune.jpg'),
    ('iPhone 14 256Go', 172, 6.7, 4, 1199.00, 'Apple Store', 'Apple', 1, 38, 'iphone14rouge.jpg'),
    ('iPhone 14 Pro 512Go', 206, 6.1, 11, 1529.00, 'Apple Store', 'Apple', 1, 25, 'iphone14proviolet.jpg'),
    ('iPhone 14 Pro Max 1To', 240, 6.7, 5, 1829.00, 'Apple Store', 'Apple', 1, 12, 'iphone14promaxgold.jpg'),
    ('iPhone 15 128Go', 171, 6.1, 7, 1099.00, 'Apple Store', 'Apple', 1, 65, 'iphone15rose.jpg'),
    ('iPhone 15 Plus 256Go', 201, 6.7, 2, 1299.00, 'Apple Store', 'Apple', 1, 42, 'iphone15plusbleu.jpg'),
    ('iPhone 15 Pro 256Go', 191, 6.1, 1, 1449.00, 'Apple Store', 'Apple', 1, 35, 'iphone15pronoir.jpg'),
    ('iPhone 15 256Go', 221, 6.7, 6, 1669.00, 'Apple Store', 'Apple', 1, 28, 'iphone15jaune.jpg'),
    ('iPhone 16 256Go', 175, 6.1, 10, 1199.00, 'Apple Store', 'Apple', 1, 75, 'iphone16blanc.jpg'),
    ('iPhone 16 Pro 256Go', 190, 6.1, 1, 1499.00, 'Apple Store', 'Apple', 1, 48, 'iphone16pro.jpg'),
    ('iPhone 16 Pro Max 1To', 220, 6.7, 8, 1799.00, 'Apple Store', 'Apple', 1, 22, 'iphone16promaxtitan.jpg'),
    ('iPhone 16 Pro 512Go', 195, 6.1, 3, 1649.00, 'Apple Store', 'Apple', 1, 31, 'iphone16proargent.jpg'),
    ('iPhone 16 Pro Max 256Go', 225, 6.7, 1, 1649.00, 'Apple Store', 'Apple', 1, 40, 'iphone16promaxnoir.jpg');

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

INSERT INTO etat(libelle) VALUES
    ('En cours de traitement'),
    ('Expédiée'),
    ('Livrée');

INSERT INTO ligne_panier (utilisateur_id, telephone_id, date_ajout, quantite) VALUES
    (2, 9, '2024-02-23 11:30:00', 1),
    (2, 10, '2024-02-23 11:35:00', 2),
    (2, 13, '2024-02-23 11:40:00', 1),
    (2, 16, '2024-02-23 11:45:00', 1);

INSERT INTO adresse (utilisateur_id, rue, ville, code_postal, pays, type_adresse) VALUES
    (1, '10 Rue de la Paix', 'Paris', '75001', 'France', 'livraison'),
    (2, '25 Avenue des Champs', 'Lyon', '69002', 'France', 'Facturation'),
    (3, '5 Boulevard Haussmann', 'Marseille', '13008', 'France', 'livraison');

INSERT INTO commande (date_achat, adresse_facturation_id, adresse_livraison_id, utilisateur_id, etat_id) VALUES
    ('2025-02-01 14:30:00', 1, 1, 2, 1),
    ('2025-02-05 09:15:00', 2, 2, 1, 2),
    ('2025-02-10 18:45:00', 3, 3, 3, 3);

INSERT INTO ligne_commande (commande_id, telephone_id, quantite, prix) VALUES
    (1, 1, 2, 909.00),
    (1, 4, 1, 809.00),
    (2, 6, 3, 1199.00),
    (3, 9, 1, 1099.00),
    (3, 12, 2, 1449.00);

INSERT INTO paiement (commande_id, montant, date_paiement, methode, statut) VALUES
    (1, 1718.00, '2025-02-01 15:00:00', 'Carte Bancaire', 'Validé'),
    (2, 3597.00, '2025-02-05 10:00:00', 'PayPal', 'En attente'),
    (3, 3997.00, '2025-02-10 19:00:00', 'Virement', 'Refusé');

INSERT INTO historique (utilisateur_id, telephone_id, date_consultation) VALUES
    (1, 1, '2025-01-01 12:00:00'),
    (2, 3, '2025-01-05 16:30:00'),
    (3, 5, '2025-01-10 09:00:00');

INSERT INTO note (utilisateur_id, telephone_id, note) VALUES
    (1, 1, 5),
    (2, 3, 4),
    (3, 5, 3);

INSERT INTO commentaire (utilisateur_id, telephone_id, texte, date_publication) VALUES
    (1, 1, 'Super téléphone !', '2025-02-01 12:00:00'),
    (2, 3, 'Bon rapport qualité/prix.', '2025-02-05 14:30:00'),
    (3, 5, 'Un peu cher mais performant.', '2025-02-10 18:00:00');

INSERT INTO liste_envie (utilisateur_id, telephone_id, date_consultation) VALUES
    (2, 15, '2024-02-20 10:15:00'),
    (3, 13, '2024-02-21 14:30:00'),
    (2, 14, '2024-02-22 09:45:00'),
    (2, 17, '2024-02-22 16:20:00'),
    (3, 11, '2024-02-23 11:30:00'),
    (3, 9, '2024-02-23 13:45:00'),
    (3, 16, '2024-02-23 15:00:00');
