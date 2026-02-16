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
    9 : ("Easy ++++", 5, 0.9), 
    8 : ("Easy +++", 10, 0.8), 
    7 : ("Easy ++", 15, 0.7), 
    6 : ("Easy +", 20, 0.6), 
    5 : ("Normal", 25, 0.5), 
    4 : ("Difficult +", 30, 0.4), 
    3 : ("Difficult ++", 35, 0.3), 
    2 : ("Difficult +++", 40, 0.2), 
    1 : ("Difficult ++++", 45, 0.1)
}

# Touches de mouvement
MOVES = {
    "z" : (-1, 0), # Haut
    "s" : (1, 0),  # Bas
    "q" : (0, -1), # Gauche
    "d" : (0, 1),  # Droite
}