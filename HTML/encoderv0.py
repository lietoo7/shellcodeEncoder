import sys
import os
import base64
import argparse
import random
import string

# --- Configuration ---
OUTPUT_FILE = "jesuiscacher.html"
# Détermine la fréquence d'injection (e.g., insérer un caractère tous les N caractères de l'hôte)
# Un nombre plus grand augmente la discrétion.
INJECTION_RATE = 200

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
    
    # Structure du commentaire : # La clé 'stg_c' permet au décodeur d'identifier ce type de payload.
    comment = f""
    return comment

# ----------------------------------------------------
# 3.1.3 Fonction creer_faussevariable(caractere) (BF007)
# ----------------------------------------------------
def creer_faussevariable(caractere: str) -> str:
    """
    Encapsule un caractère du payload dans une fausse variable JavaScript ou CSS.
    L'alternance entre JS et CSS et l'aléatoire augmentent la discrétion.
    """
    injection_type = random.choice(['js', 'css'])
    # Génère un ID aléatoire unique pour le nom de la variable
    random_id = ''.join(random.choices(string.ascii_letters, k=5)) + str(random.randint(100, 999))

    if injection_type == 'js':
        # Ex: <script>var _hD1e45 = 'S';</script>
        return f"<script>var _{random_id} = '{caractere}';</script>"
    else: # CSS
        # Ex: <style> :root {{--c5H9j: 'S';}} </style>
        # Note: L'utilisation de :root garantit que la variable est globale mais non utilisée.
        return f"<style> :root {{--{random_id}: '{caractere}';}} </style>"

# ----------------------------------------------------
# 3.1.1 Script Principal (Encoder.py)
# ----------------------------------------------------
def encode_html_steganography(input_html_path: str, payload_str: str):
    """
    Fonction principale pour encoder le payload dans le fichier HTML hôte.
    (BF001, BF003, BF004, BF005)
    """
    print(f"Debut de l'encodage de '{payload_str}'...")

    # 1. Encodage du Payload (BF002)
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
    
    # Vérification simple pour s'assurer que le contenu est suffisant
    if len(html_content) < len(encoded_payload) * INJECTION_RATE * 0.5:
         print(f"Avertissement : Le fichier hote pourrait etre trop court ({len(html_content)} octets) pour inserer discretement le payload.")


    # 3. Iteration et Placement (BF004, BF005)
    
    output_content = ""
    payload_index = 0
    host_index = 0
    
    # Selectionne aleatoirement les types d'injection pour alterner (BF005)
    injection_functions = [creer_fauxcommentaire, creer_faussevariable]
    random.shuffle(injection_functions)
    
    # Iteration sur le contenu du fichier HTML
    while host_index < len(html_content):
        # On ajoute le caractere hote actuel au fichier de sortie
        output_content += html_content[host_index]
        
        # Condition d'injection : si nous avons encore des caracteres a cacher
        if payload_index < len(encoded_payload):
            
            # Condition de frequence : inserer tous les INJECTION_RATE caracteres
            if host_index > 0 and host_index % INJECTION_RATE == 0:
                
                # Recupere le prochain caractere a cacher
                char_to_hide = encoded_payload[payload_index]
                
                # Choix et execution de la fonction d'injection (BF006 ou BF007)
                injection_func = injection_functions[payload_index % len(injection_functions)]
                
                injected_code = injection_func(char_to_hide)
                
                # Injection dans le contenu de sortie
                output_content += injected_code
                
                print(f"   -> Injecte '{char_to_hide}' (Type: {injection_func.__name__}, Index Hote: {host_index})")
                
                payload_index += 1
        
        host_index += 1

    # Verification si tout le payload a ete insere
    if payload_index < len(encoded_payload):
        print(f"Erreur : Seulement {payload_index}/{len(encoded_payload)} caracteres inseres. Le fichier hote etait trop court ou le taux d'injection est trop eleve.")
    else:
        print("Tous les caracteres du payload ont ete inseres avec succes.")

    # 4. Ecriture du Fichier de Sortie (BF003)
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Fichier steganographie cree : {OUTPUT_FILE}")
        print(f"Verifiez l'integrite visuelle (UC005) : {input_html_path} vs {OUTPUT_FILE}")
    except Exception as e:
        print(f"Erreur lors de l'ecriture du fichier de sortie : {e}")

# ----------------------------------------------------
# Interface Utilisateur (Ligne de Commande) (3.3)
# ----------------------------------------------------
if __name__ == "__main__":
    # Utilisation du module argparse pour une meilleure interface CLI (3.3)
    parser = argparse.ArgumentParser(
        description="Outil de Steganographie HTML. Encode une chaine de caracteres dans un fichier HTML hote.",
        epilog="Exemple: python Encoder.py mapage.html 'Mon message secret'"
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
