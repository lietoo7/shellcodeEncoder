import sys
import os
import base64
import argparse
import random
import string

# --- Configuration ---
OUTPUT_FILE = "jesuiscacher.html"
# Le taux est basé sur les caractères HÔTES parcourus entre chaque tentative d'injection.
INJECTION_RATE = 50

# LISTE DES BALISES DE FIN SÛRES : L'injection aura lieu APRES ces séquences.
# Cela garantit que le code est placé entre des blocs HTML structurels.
SAFE_CLOSING_TAGS = [
    '</div>', '</p>', '</li>', '</span>', '</form>', '</header>', 
    '</footer>', '</section>', '</body>', '</html>', '</table>', 
    '</pre>', '</article>',
]


# ----------------------------------------------------
# 3.1.2 Fonction creer_fauxcommentaire(caractere) (BF006)
# ----------------------------------------------------
def creer_fauxcommentaire(caractere: str) -> str:
    """
    Encapsule un caractère du payload dans un commentaire HTML.
    Ajoute du padding aléatoire pour la discrétion.
    """
    # Génère une chaîne aléatoire courte pour le padding dans le commentaire
    padding = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
    
    # Structure du commentaire : La clé 'stg_c' permet au décodeur d'identifier ce type de payload.
    comment = f""
    return comment

# ----------------------------------------------------
# 3.1.3 Fonction creer_faussevariable(caractere) (BF007)
# ----------------------------------------------------
def creer_faussevariable(caractere: str) -> str:
    """
    Encapsule un caractère du payload dans une fausse variable JavaScript ou CSS.
    """
    injection_type = random.choice(['js', 'css'])
    random_id = ''.join(random.choices(string.ascii_letters, k=5)) + str(random.randint(100, 999))

    if injection_type == 'js':
        # Ex: <script>var _hD1e45 = 'S';</script>
        return f"<script>var _{random_id} = '{caractere}';</script>"
    else: # CSS
        # Ex: <style> :root {{--c5H9j: 'S';}} </style>
        return f"<style> :root {{--{random_id}: '{caractere}';}} </style>"

# ----------------------------------------------------
# 3.1.1 Script Principal (Encoder.py) - LOGIQUE D'INJECTION FINALE
# ----------------------------------------------------
def encode_html_steganography(input_html_path: str, payload_str: str):
    """
    Fonction principale pour encoder le payload dans le fichier HTML hôte.
    Cible l'injection après les balises de fin structurelles.
    """
    print(f"Debut de l'encodage de '{payload_str}'...")

    # 1. Encodage du Payload
    try:
        encoded_payload = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')
        print(f"Payload encode en Base64 : {encoded_payload} ({len(encoded_payload)} caracteres)")
    except Exception as e:
        print(f"Erreur lors de l'encodage Base64 : {e}")
        return

    # 2. Lecture et Initialisation
    try:
        with open(input_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Fichier source non trouve : {input_html_path}")
        return
    
    if len(html_content) < len(encoded_payload) * INJECTION_RATE * 0.5:
        print(f"Avertissement : Le fichier hote pourrait etre trop court ({len(html_content)} octets) pour inserer discretement le payload.")


    # 3. Iteration et Placement (Amélioré)
    output_content = ""
    payload_index = 0
    host_index = 0
    injection_counter = 0 # Compteur pour respecter le taux d'injection
    
    injection_functions = [creer_fauxcommentaire, creer_faussevariable]
    random.shuffle(injection_functions)
    
    # Iteration sur le contenu du fichier HTML
    while host_index < len(html_content):
        current_char = html_content[host_index]
        
        # 1. On ajoute le caractere hote actuel au fichier de sortie
        output_content += current_char
        host_index += 1
        injection_counter += 1
        
        # Condition d'injection : si nous avons encore des caracteres a cacher
        if payload_index < len(encoded_payload):
            
            # Condition de frequence : on vérifie la fréquence avant de chercher un point sûr
            if injection_counter >= INJECTION_RATE:
                
                # Condition de securite : Verifier si nous venons de terminer l'écriture d'une balise de fin sûre
                injected = False
                for tag in SAFE_CLOSING_TAGS:
                    if output_content.endswith(tag):
                        
                        # Point de repère sûr trouvé. Injection
                        injection_counter = 0 # Reset du compteur de fréquence
                        
                        char_to_hide = encoded_payload[payload_index]
                        injection_func = injection_functions[payload_index % len(injection_functions)]
                        injected_code = injection_func(char_to_hide)
                        
                        # Injection dans le contenu de sortie, immédiatement APRES la balise de fin
                        output_content += injected_code
                        
                        print(f"    -> Injecte '{char_to_hide}' (Type: {injection_func.__name__}, Index Hote: {host_index-1}) APRES balise de fin '{tag}'")
                        
                        payload_index += 1
                        injected = True
                        break # Sortir de la boucle des tags pour continuer le traitement hôte

                if injected:
                    continue # Passe à l'itération suivante de la boucle while
        
        # Ce bloc de code ne s'exécutera que si le payload est plus long que le contenu HTML.
        # Il est conservé pour s'assurer que tout le payload est écrit, même si ce n'est pas "discret".
        elif payload_index < len(encoded_payload) and host_index == len(html_content):
             print(f"Avertissement : Fin de fichier atteint. Ajout du reste du payload ({len(encoded_payload) - payload_index} caractères) à la toute fin.")
             while payload_index < len(encoded_payload):
                 char_to_hide = encoded_payload[payload_index]
                 injection_func = injection_functions[payload_index % len(injection_functions)]
                 output_content += injection_func(char_to_hide)
                 payload_index += 1
                 
             break 

    # 4. Finalisation
    if payload_index < len(encoded_payload):
        print(f"Erreur : Seulement {payload_index}/{len(encoded_payload)} caracteres inseres. Le fichier hôte était trop court pour insérer discrètement tout le payload.")
    else:
        print("Tous les caracteres du payload ont ete inseres avec succes.")

    # 5. Ecriture du Fichier de Sortie
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Fichier steganographie cree : {OUTPUT_FILE}")
        print(f"Verification de l'integrite visuelle (UC005) : L'affichage devrait désormais être préservé.")
    except Exception as e:
        print(f"Erreur lors de l'ecriture du fichier de sortie : {e}")

# ----------------------------------------------------
# Interface Utilisateur (Ligne de Commande) (3.3)
# ----------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Outil de Steganographie HTML. Encode une chaine de caracteres dans un fichier HTML hote.",
        epilog="Exemple: python encoder.py mapage.html 'Mon message secret'"
    )
    parser.add_argument(
        "html_source",
        help="Chemin vers le fichier HTML hote a utiliser (e.g., mapage.html)."
    )
    parser.add_argument(
        "payload",
        help="La chaine de caracteres secrete a cacher (le payload)."
    )
    
    args = parser.parse_args()
    
    encode_html_steganography(args.html_source, args.payload)
