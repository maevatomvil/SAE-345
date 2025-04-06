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
DROP TABLE IF EXISTS declinaison_telephone;
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
    description TEXT,
    image VARCHAR(50),
    PRIMARY KEY(id_telephone),
    FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur),
    FOREIGN KEY (type_telephone_id) REFERENCES type_telephone(id_type_telephone)
);

CREATE TABLE declinaison_telephone (
    id_declinaison INT AUTO_INCREMENT,
    telephone_id INT,
    taille VARCHAR(20),
    couleur_id INT,
    stock INT,
    prix DECIMAL(15,2),
    PRIMARY KEY(id_declinaison),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone),
    FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur)
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
    declinaison_id INT,
    date_ajout DATETIME,
    quantite INT,
    prix_unitaire DECIMAL(15,2),
    PRIMARY KEY (utilisateur_id, telephone_id, date_ajout),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (telephone_id) REFERENCES telephone(id_telephone),
    FOREIGN KEY (declinaison_id) REFERENCES declinaison_telephone(id_declinaison)
);

CREATE TABLE adresse (
    id_adresse INT AUTO_INCREMENT,
    utilisateur_id INT,
    nom varchar(255),
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
    valider BOOLEAN,
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

INSERT INTO telephone (nom_telephone, poids, taille, couleur_id, prix_telephone, fournisseur, marque, type_telephone_id, stock, description, image) VALUES
    ('iPhone 13 128Go', 174, 6.1, 10, 909.00, 'Apple Store', 'Apple', 1, 45, 'vksdsflnvfjbvsfk','iphone13blanc.jpg'),
    ('iPhone 13 Pro 256Go', 204, 6.1, 9, 1259.00, 'Apple Store', 'Apple', 1, 28, 'vksdsflnvfjbvsfk', 'iphone13provert.jpg'),
    ('Nokia 3310 (2017)', 133, 2.4, 1, 59.99, 'Nokia', 'Nokia', 3, 10, 'Téléphone classique avec une batterie longue durée.', 'nokia33102017.jpg'),
    ('Nokia 3310', 133, 2.4, 2, 59.99, 'Nokia', 'Nokia', 3, 15, 'Modèle emblématique avec jeu Snake.', 'nokia3310.jpg'),
    ('iPhone 13 Mini 128Go', 140, 5.4, 1, 809.00, 'Apple Store', 'Apple', 1, 15, 'vksdsflnvfjbvsfk','iphone13mininoir.jpg'),
    ('iPhone 14 256Go', 172, 6.7, 4, 1199.00, 'Apple Store', 'Apple', 1, 38, 'vksdsflnvfjbvsfk','iphone14rouge.jpg'),
    ('iPhone 14 Pro 512Go', 206, 6.1, 11, 1529.00, 'Apple Store', 'Apple', 1, 25, 'vksdsflnvfjbvsfk','iphone14proviolet.jpg'),
    ('iPhone 14 Pro Max 1To', 240, 6.7, 5, 1829.00, 'Apple Store', 'Apple', 1, 12, 'vksdsflnvfjbvsfk','iphone14promaxgold.jpg'),
    ('Nokia 2660 Flip', 123, 2.8, 3, 79.99, 'Nokia', 'Nokia', 2, 20, 'Téléphone à clapet pratique pour seniors.', 'nokia2660flip.jpg'),
    ('Doro 2820', 110, 2.8, 4, 89.99, 'Doro', 'Doro', 2, 25, 'Téléphone adapté aux personnes âgées avec assistance SOS.', 'doro2820blanc.jpg'),
    ('iPhone 15 128Go', 171, 6.1, 7, 1099.00, 'Apple Store', 'Apple', 1, 65, 'vksdsflnvfjbvsfk','iphone15rose.jpg'),
    ('iPhone 15 Pro 256Go', 191, 6.1, 1, 1449.00, 'Apple Store', 'Apple', 1, 35, 'vksdsflnvfjbvsfk','iphone15pronoir.jpg'),
    ('iPhone 15 256Go', 221, 6.7, 6, 1669.00, 'Apple Store', 'Apple', 1, 28, 'vksdsflnvfjbvsfk','iphone15jaune.jpg'),
    ('iPhone 16 256Go', 175, 6.1, 10, 1199.00, 'Apple Store', 'Apple', 1, 75, 'vksdsflnvfjbvsfk','iphone16blanc.jpg'),
    ('iPhone 16 Pro 256Go', 190, 6.1, 1, 1499.00, 'Apple Store', 'Apple', 1, 48, 'vksdsflnvfjbvsfk','iphone16pronoir.jpg'),
    ('iPhone 16 Pro Max 1To', 220, 6.7, 8, 1799.00, 'Apple Store', 'Apple', 1, 22, 'vksdsflnvfjbvsfk','iphone16promaxtitan.jpg'),
    ('iPhone 16 Pro 512Go', 195, 6.1, 3, 1649.00, 'Apple Store', 'Apple', 1, 31, 'vksdsflnvfjbvsfk','iphone16proargent.jpg'),
    ('Alcatel XL585 Solo', 105, 2.6, 5, 49.99, 'Alcatel', 'Alcatel', 4, 30, 'Téléphone avec grandes touches pour une utilisation facile.', 'alcatelXL585solo.jpg'),
    ('Essentielb Tribu Duo-R V3', 120, 2.4, 6, 39.99, 'Essentielb', 'Essentielb', 4, 18, 'Téléphone simple et efficace avec double SIM.', 'essentielbtribuduo-Rv3.jpg');

# Ajout des déclinaisons pour les iPhones
INSERT INTO declinaison_telephone (telephone_id, taille, couleur_id, stock, prix) VALUES
    # iPhone 15
    (11, '128Go', 7, 20, 1099.00),  # Rose
    (11, '256Go', 7, 15, 1199.00),
    (11, '512Go', 7, 10, 1399.00),
    (11, '128Go', 2, 18, 1099.00),  # Bleu
    (11, '256Go', 2, 12, 1199.00),
    (11, '512Go', 2, 8, 1399.00),
    
    # iPhone 15 Pro
    (12, '128Go', 1, 25, 1349.00),  # Noir
    (12, '256Go', 1, 20, 1449.00),
    (12, '512Go', 1, 15, 1649.00),
    (12, '1To', 1, 10, 1849.00),
    (12, '128Go', 8, 22, 1349.00),  # Titane
    (12, '256Go', 8, 18, 1449.00),
    (12, '512Go', 8, 12, 1649.00),
    (12, '1To', 8, 8, 1849.00),
    
    # iPhone 16
    (14, '128Go', 10, 30, 1099.00),  # Blanc
    (14, '256Go', 10, 25, 1199.00),
    (14, '512Go', 10, 20, 1399.00),
    (14, '128Go', 3, 28, 1099.00),  # Argent
    (14, '256Go', 3, 22, 1199.00),
    (14, '512Go', 3, 18, 1399.00),
    
    # Pour les téléphones non-iPhone (déclinaison unique)
    (3, 'taille unique', 1, 10, 59.99),   # Nokia 3310
    (9, 'taille unique', 3, 20, 79.99),   # Nokia 2660 Flip
    (10, 'taille unique', 4, 25, 89.99);  # Doro 2820

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

INSERT INTO ligne_panier (utilisateur_id, telephone_id, declinaison_id, date_ajout, quantite, prix_unitaire) VALUES
    (2, 9, 1, '2024-02-23 11:30:00', 1, 909.00),
    (2, 10, 2, '2024-02-23 11:35:00', 2, 1199.00),
    (2, 13, 1, '2024-02-23 11:40:00', 1, 809.00),
    (2, 16, 1, '2024-02-23 11:45:00', 1, 1199.00);

INSERT INTO adresse (utilisateur_id, nom, rue, ville, code_postal, pays, type_adresse) VALUES
    (1,'admin', '10 Rue de la Paix', 'Paris', '75001', 'France', 'livraison'),
    (2,'client', '25 Avenue des Champs', 'Lyon', '69002', 'France', 'Facturation'),
    (3,'client2', '5 Boulevard Haussmann', 'Marseille', '13008', 'France', 'livraison');

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
    (2, 3, 4),
    (3, 5, 3);

INSERT INTO commentaire (utilisateur_id, telephone_id, texte, date_publication, valider) VALUES
    (2, 3, 'Bon rapport qualité/prix.', '2025-02-05 14:30:00', 0),
    (3, 5, 'Un peu vieux mais pratique.', '2025-02-10 18:00:00', 0);

INSERT INTO liste_envie (utilisateur_id, telephone_id, date_consultation) VALUES
    (2, 15, '2024-02-20 10:15:00'),
    (3, 13, '2024-02-21 14:30:00'),
    (2, 14, '2024-02-22 09:45:00'),
    (2, 17, '2024-02-22 16:20:00'),
    (3, 11, '2024-02-23 11:30:00'),
    (3, 9, '2024-02-23 13:45:00'),
    (3, 16, '2024-02-23 15:00:00');