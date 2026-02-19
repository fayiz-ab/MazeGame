# Fichier contenant les fonctions et la gestion des sauvegardes
 
import random
import json
import settings  

# --- GÉNÉRATION ET FONCTIONS ---

def create_maze(size, path_probability): 
    # Génère une grille de labyrinthe de manière aléatoire
    while True : 
        maze = [[None for _ in range(size)] for _ in range(size)] # Initialisation d'une matrice vide pour représenter le labyrinthe
        last_index = size - 1 
        corners = [[0,0], [0,last_index], [last_index,0], [last_index,last_index]] # Création d'une liste avec les coordonnées des quatre coins du labyrinthe, pour placer l'entrée et la sortie

        entry = random.choice(corners) # Choix aléatoire de l'entrée du labyrinthe
        maze[entry[0]][entry[1]] = 0
        corners.remove(entry) # On retire l'entrée de la liste des coins, pour pouvoir choisir un autre coin comme sortie 

        exit = random.choice(corners) # Choix aléatoire de la sortie
        maze[exit[0]][exit[1]] = 2

        nb_elements = size**2 
        nb0 = int(nb_elements*path_probability) # Nombre de 0 (chemins)
        nb1 = nb_elements - nb0 # Nombre de 1 (murs)
        
        list_elements = [0]*(nb0-2) + [1]*nb1 # On crée une liste contenant le nombre de 0 et de 1 correspondant à la probabilité de 0 rentrée par l'utilisateur (on retire deux 0, car on les a déjà associés à l'entrée et la sortie)
        random.shuffle(list_elements) 

        index = 0
        for i in range(size):
            for j in range(size):
                if [i,j] != entry and [i,j] != exit :
                    maze[i][j] = list_elements[index]  # On associe à chaque élément du labyrinthe une valeur de la liste de 0 et 1, triée au hasard, en respectant ainsi la probabilité de chemin donnée
                    index += 1

        if is_solvable(maze, entry) : # On ne renvoie le labyrinthe que s'il est possible d'aller de son entrée à sa sortie
            return maze, entry

def is_solvable(maze, entry) :
    # Vérifie si le labyrinthe possède un chemin valide, permettant d'accéder à la sortie
    visit_history = [entry] # Liste des cases du labyrinthe déjà visitées
    visit_queue = [entry] # File d'attente des prochaines cases à explorer

    while len(visit_queue) != 0 : # Algorithme de BFS 
        v = visit_queue[0] # Case du labyrinthe qu'on explore

        if maze[v[0]][v[1]] == 2 : # Si la case qu'on explore est la sortie, alors il existe un chemin menant à elle et on renvoie True
            return True
        
        else : 
            v_left = [v[0] - 1, v[1]]
            v_right = [v[0] + 1, v[1]]
            v_up = [v[0], v[1] + 1]
            v_down = [v[0], v[1] - 1]

            neighboors = [v_left, v_right, v_up, v_down]

            for e in neighboors :
                condition_len = e[0] >= 0 and e[0] < len(maze) and e[1] >= 0 and e[1] < len(maze)
                if condition_len and maze[e[0]][e[1]] != 1 and e not in visit_history : 
                    visit_history.append(e)
                    visit_queue.append(e)
        visit_queue.pop(0)

    return False

def create_perso(start):
    # Création du dictionnaire représentant le joueur 
    return {"char": "o", "x": start[0], "y": start[1]}

def update_p(maze, letter, p):
    # Mise à jour de la position du joueur si le mouvement est valide
    if letter not in settings.MOVES : 
        return "Please enter a correct movement letter : 'z', 's', 'q', or 'd'."
    
    dx, dy = settings.MOVES[letter] 
    newx, newy = p["x"] + dx, p["y"] + dy # Nouvelles coordonnées du joueur après le mouvement

    if not (0 <= newx < len(maze) and 0 <= newy < len(maze)) : # On vérifie que les nouvelles coordonnées sont bien dans le labyrinthe
        return "You can't exit from the edges of the maze."

    if maze[newx][newy] == 1 : # On vérifie que l'utilisateur ne va pas sur une case contenant un mur
        return "You can't go on a wall."

    p["x"], p["y"] = newx, newy

def create_items(maze, num_items, entry):
    # Place des objets (I) aléatoirement sur les cases libres du labyrinthe
    list_items = []
    cases_free = []
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] != 1 and maze[i][j] != 2 and maze[i][j] != entry :
                cases_free.append((i,j))
    if num_items <= len(cases_free) :
        for k in range(num_items):
            (x,y) = random.choice(cases_free)
            list_items.append((x,y))
            cases_free.remove((x,y))
    return list_items
        
def collect_item(perso, items):
    # Vérifie si le joueur est sur un objet, et si c'est le cas, le ramasse 
    items_collected = 0
    for i in items[:] : 
        if (perso["x"], perso["y"]) == i :
            items.remove(i)
            items_collected += 1
            print("Item collected !")
            return items_collected
    return items_collected

def level(n): 
    # Charge les paramètres du niveau n depuis settings.py et génère un labyrinthe dont la taille et la probabilité de chemin sont associées à la difficulté 
    if 1 <= n <= 9 :
        size = settings.DIFFICULTY[n][1]
        prob = settings.DIFFICULTY[n][2]
        return create_maze(size, path_probability=prob)  

# --- TÉLÉPORTEURS ---

def create_teleport(maze, entry, n):
    # Génère des paires de téléporteurs sur la grille
    teleporter = {} 
    cases_free = [] 
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] != 1 and maze[i][j] != 2 and maze[i][j] != entry :
                cases_free.append((i,j)) 
    
    if n < len(cases_free) :
        for k in range(n):
            if len(cases_free) < 2: break 
            (xt_1, yt_1) = random.choice(cases_free) 
            cases_free.remove((xt_1, yt_1))
            (xt_2, yt_2) = random.choice(cases_free)
            cases_free.remove((xt_2, yt_2))
            teleporter[(xt_1, yt_1)] = (xt_2, yt_2)
            teleporter[(xt_2, yt_2)] = (xt_1, yt_1)
    return teleporter            

def teleport(p, teleporter):
    # Vérifie si le joueur est sur un téléporteur et, si c'est le cas, déplace le joueur au téléporteur associé
    pos = (p["x"], p["y"])

    if pos in teleporter: # On vérifie si on est sur une entrée de téléporteur
        (p["x"], p["y"]) = teleporter[pos]

# --- AFFICHAGE ---

def draw_maze(maze, items, p, teleporters):
    # Affiche le labyrinthe, le joueur, les objets et les téléporteurs dans la console
    dico = settings.SYMBOLS
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if i == p["x"] and j == p["y"] :
                print(p["char"], end=" ") # Affichage du joueur
            elif (i,j) in items:
                print("I", end=" ") # Affichage d'un objet
            elif (i, j) in teleporters.keys() or (i, j) in teleporters.values():
                print("T", end=" ") # Affichage d'un téléporteur
            else :
                print(dico[maze[i][j]], end=" ") 
        print()

# --- GESTION DES SAUVEGARDES (JSON) ---

# Chargement de la progression au démarrage du script
try:
    with open(settings.PROGRESS_FILE, "r") as file:
        saved_progress = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    # Si le fichier n'existe pas encore on crée un dictionnaire vide
    saved_progress = {}

# Chargement des scores 
try:
    with open(settings.SPEEDS_FILE, "r") as file:
        data = json.load(file)
        # On convertit les clés en int pour les niveaux car elles sont stockées en strings par JSON
        speed_dico = {int(k): v for k, v in data.items()}
except (FileNotFoundError, json.JSONDecodeError):
    speed_dico = {i: {} for i in range(1, 10)}

def save_progress(name, level_user): 
    # auvegarde le niveau actuel du joueur dans le fichier JSON
    saved_progress[name] = level_user 
    with open(settings.PROGRESS_FILE, "w") as file:
        json.dump(saved_progress, file, indent=4)

def get_saved_level(name):
    # Récupère le niveau sauvegardé d'un joueur
    return saved_progress.get(name)

def save_speed(username, user_time, level_n):
    # Enregistre le temps du joueur (l'initialise ou le met à jour s'il a battu son record)
    if level_n not in speed_dico:
        speed_dico[level_n] = {}
    
    # On ne met à jour que si le nouveau temps est meilleur 
    if username in speed_dico[level_n]:
        if user_time < speed_dico[level_n][username]:
            speed_dico[level_n][username] = round(user_time, 2)
    else:
        speed_dico[level_n][username] = round(user_time, 2)

    with open(settings.SPEEDS_FILE, "w") as file:
        json.dump(speed_dico, file, indent=4)

def print_speed_ranking(level_n):
    # Affiche le classement des meilleurs temps pour un niveau donné
    if level_n in speed_dico and speed_dico[level_n]: 
        sorted_players = sorted(speed_dico[level_n].items(), key=lambda x: x[1])
        print(f"Level {settings.DIFFICULTY[level_n][0]} Ranking")
        for rank, (player, time_val) in enumerate(sorted_players):
            print(f"Rank {rank+1} - {player} : Time {time_val}s")
    else : 
        print(f"No players have completed level {settings.DIFFICULTY[level_n][0]} yet.")