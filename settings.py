# Fichier contenant toutes les constantes et la configuration du jeu

# Fichiers de sauvegarde des données (en JSON)
PROGRESS_FILE = "saved_progress.json"
SPEEDS_FILE = "saved_speeds.json"

# Dictionnaire des symboles pour l'affichage du labyrinthe dans la console
# 0 = Chemin, 1 = Mur (#), 2 = Sortie (S)
SYMBOLS = {0: ' ', 1: '#', 2: 'S'}

# Configuration de la difficulté du jeu
# Format : Chiffre du niveau : ("Nom", Taille du labyrinthe, Probabilité de chemin)
# Plus la probabilité est faible, plus il y a de murs
DIFFICULTY = {
    9 : ("Easy ++++", 7, 0.90), 
    8 : ("Easy +++", 9, 0.85), 
    7 : ("Easy ++", 11, 0.80), 
    6 : ("Easy +", 13, 0.75), 
    5 : ("Normal", 15, 0.70), 
    4 : ("Difficult +", 17, 0.65), 
    3 : ("Difficult ++", 20, 0.60), 
    2 : ("Difficult +++", 22, 0.55), 
    1 : ("Difficult ++++", 25, 0.50)
}

# Touches de mouvement
MOVES = {
    "z" : (-1, 0), # Haut
    "s" : (1, 0),  # Bas
    "q" : (0, -1), # Gauche
    "d" : (0, 1),  # Droite
}