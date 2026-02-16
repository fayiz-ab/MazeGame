import time
import settings
import game_engine as engine

def play_game():
    # Gère le déroulement d'une partie 
    n = 9 # Niveau par défaut (niveau le plus simple)
    
    # Initialisation du premier niveau
    labyrinthe_lvl, game_entry = engine.level(n)
    joueur = engine.create_perso(game_entry)
    items_maze = engine.create_items(labyrinthe_lvl, 10-n, game_entry)
    teleporters_maze = engine.create_teleport(labyrinthe_lvl, game_entry, 10-n)

    username = input("Enter your username : ")
    
    # Vérification ce la sauvegarde
    saved_level = engine.get_saved_level(username)
    if saved_level:
        while True:
            print(f"You reached level {settings.DIFFICULTY[saved_level][0]}. Do you want to resume ?")
            answer = input("Yes or No ? ")
            if answer.lower() == "yes":
                n = saved_level
                # Rechargement du niveau sauvegardé
                labyrinthe_lvl, game_entry = engine.level(n)
                joueur = engine.create_perso(game_entry)
                items_maze = engine.create_items(labyrinthe_lvl, 10-n, game_entry)
                teleporters_maze = engine.create_teleport(labyrinthe_lvl, game_entry, 10-n)
                engine.draw_maze(labyrinthe_lvl, items_maze, joueur, teleporters_maze)
                break
            elif answer.lower() == "no":
                # On recommence au premier niveau (n=9)
                engine.draw_maze(labyrinthe_lvl, items_maze, joueur, teleporters_maze)
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.") 
    else: # Si l'utilisateur n'avait pas joué auparavant on enregistre son nom et on lui crée un labyrinthe du premier niveau
        engine.save_progress(username, n)
        engine.draw_maze(labyrinthe_lvl, items_maze, joueur, teleporters_maze)

    start_time = time.time()

    # Boucle du jeu
    while n >= 1:
        d = input("Enter move (z,q,s,d) or 'e' to quit: ")

        if d == "e":
            print("Quitting to main menu.")
            return

        # Mise à jour de la position et des intéractions
        error = engine.update_p(labyrinthe_lvl, d, joueur) # On tente de faire le mouvement et on capture une erreur éventuelle (la fonction update_p renvoie None si le mouvement est possible, ou une chaîne de caractère indiquant l'erreur si le mouvement est impossible)        
        if error: # S'il y a une erreur (donc si ce n'est pas None), on l'affiche
            print(f"{error}")
        engine.collect_item(joueur, items_maze)
        engine.teleport(joueur, teleporters_maze)
        engine.draw_maze(labyrinthe_lvl, items_maze, joueur, teleporters_maze)

        # Victoire du niveau
        if labyrinthe_lvl[joueur["x"]][joueur["y"]] == 2:
            end_time = time.time()
            game_time = end_time - start_time
            engine.save_speed(username, game_time, n)

            print("\nCongratulations!")
            engine.print_speed_ranking(n)
            time.sleep(2)

            if n == 1:
                print("YOU FINISHED THE GAME! LEGEND!")
                break

            print("\n--- NEXT LEVEL ---")
            n -= 1
            engine.save_progress(username, n)
            
            # Création d'un nouveau labyrinthe pour le niveau suivant
            labyrinthe_lvl, game_entry = engine.level(n)
            joueur = engine.create_perso(game_entry)
            items_maze = engine.create_items(labyrinthe_lvl, 10-n, game_entry)
            teleporters_maze = engine.create_teleport(labyrinthe_lvl, game_entry, 10-n)
            
            start_time = time.time()
            engine.draw_maze(labyrinthe_lvl, items_maze, joueur, teleporters_maze)

def main_menu():
    # Affiche le menu d'accueil
    while True:
        print("\n=== Welcome to the Maze Game! ===")
        choice = input("Do you want to play? (yes/e): ")
        if choice.lower() == "yes":
            play_game() # Lancer le jeu
        elif choice.lower() == "e":
            print("Goodbye!") # Quitter le jeu
            break
        else :
            print("Invalid input. Please type 'yes' to play or 'e' to quit.")

if __name__ == "__main__":
    main_menu()