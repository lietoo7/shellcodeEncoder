import sys
import os
import base64
import argparse
import random
import string
from typing import List

# --- Configuration ---
OUTPUT_FILE = "jesuiscacher.html"

# LISTE DES BALISES DE FIN SÛRES
SAFE_CLOSING_TAGS = [
    '</div>', '</p>', '</li>', '</span>', '</form>', '</header>', 
    '</footer>', '</section>', '</body>', '</html>', '</table>', 
    '</pre>', '</article>'
]

# ----------------------------------------------------
# 3.1.2 Fonction creer_fauxcommentaire(caractere) (BF006)
# ----------------------------------------------------
def creer_fauxcommentaire(caractere: str) -> str:
    """
    Encapsule un caractère du payload dans un commentaire HTML.
    Ajoute du padding aléatoire pour la discrétion.
    """
    padding = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
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
        return f"<script>var _{random_id} = '{caractere}';</script>"
    else: # CSS
        return f"<style> :root {{--{random_id}: '{caractere}';}} </style>"

# ----------------------------------------------------
# 3.1.4 Fonction d'Auto-Correction (BF010)
# ----------------------------------------------------
def auto_patch_html_slots(html_content: str, required_slots: int, available_slots: int) -> str:
    """
    Ajoute des balises de fin structurelles pour augmenter le nombre de points d'injection.
    L'insertion se fait juste avant </body> pour minimiser l'impact visuel.
    """
    slots_needed = required_slots - available_slots
    
    # Ajout d'une marge de sécurité de 10% (minimum 100)
    safety_margin = max(100, int(slots_needed * 0.10)) 
    tags_to_add = slots_needed + safety_margin
    
    # Utilisation d'une balise ouvrante div avec display:none pour contenir les balises </p>
    # L'utilisation de </p> est privilégiée car elle crée un grand nombre de slots sûrs
    injection_chunk = f'\n\n<div style="display:none;">' + ('</p>' * tags_to_add) + '</div>\n\n'
    
    # Chercher la balise </body> pour l'insertion (commence par la fin du fichier)
    body_close_index = html_content.rfind('</body>')
    
    if body_close_index == -1:
        # Si </body> n'existe pas, on insère avant </html>
        html_close_index = html_content.rfind('</html>')
        if html_close_index != -1:
            print("    [!] Avertissement: </body> non trouvé. Insertion avant </html>.")
            return html_content[:html_close_index] + injection_chunk + html_content[html_close_index:]
        else:
            # Cas extrême : insertion à la fin du fichier
            print("    [!] Avertissement: Ni </body> ni </html> trouvé. Insertion à la fin du fichier.")
            return html_content + injection_chunk

    print(f"    [OK] Insertion de {tags_to_add} balises </p> avant </body> pour garantir l'espace.")
    
    # Insertion de la chunk juste avant </body>
    return html_content[:body_close_index] + injection_chunk + html_content[body_close_index:]


# ----------------------------------------------------
# 3.1.1 Script Principal (Encoder.py) - LOGIQUE DYNAMIQUE ET AUTONOME
# ----------------------------------------------------
def encode_html_steganography(input_html_path: str, payload_file_path: str):
    """
    Encode le contenu d'un fichier payload dans le fichier HTML hôte.
    Calcule dynamiquement les emplacements et applique un patch si nécessaire.
    """
    
    # 1. Lecture du Fichier Payload
    try:
        with open(payload_file_path, 'r', encoding='utf-8') as f:
            payload_str = f.read()
        print(f"Payload lu avec succes depuis le fichier : '{payload_file_path}' ({len(payload_str)} octets)")
    except FileNotFoundError:
        print(f"Erreur : Fichier payload non trouve : {payload_file_path}")
        return
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier payload : {e}")
        return

    print(f"Debut de l'encodage du contenu...")

    # 2. Encodage du Payload
    try:
        encoded_payload = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')
        payload_length = len(encoded_payload)
        print(f"Payload encode en Base64 : {encoded_payload[:50]}... ({payload_length} caracteres requis)")
    except Exception as e:
        print(f"Erreur lors de l'encodage Base64 : {e}")
        return

    # 3. Lecture du fichier Hôte
    try:
        with open(input_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Fichier hote non trouve : {input_html_path}")
        return
    
    # --- DÉBUT BOUCLE D'AUTOCORRECTION/SCAN ---
    
    # On itère jusqu'à ce que les slots soient suffisants (ou que la correction échoue)
    while True:
        
        # 4. Phase de Scan: Identification des Emplacements Sûrs
        safe_injection_indices: List[int] = []
        
        for tag in SAFE_CLOSING_TAGS:
            start_index = 0
            while True:
                index = html_content.find(tag, start_index)
                if index == -1:
                    break
                
                # L'emplacement sûr est immédiatement APRÈS la balise de fin
                injection_index = index + len(tag)
                safe_injection_indices.append(injection_index)
                
                start_index = injection_index

        safe_injection_indices = sorted(list(set(safe_injection_indices)))
        available_slots = len(safe_injection_indices)
        
        # 5. Phase de Vérification et d'Auto-Correction
        if available_slots < payload_length:
            
            if "AUTO-PATCH" in html_content:
                # Si le patch a déjà été appliqué et que cela ne suffit toujours pas (cas très rare), on arrête
                print(f"Erreur Fatale: L'auto-correction a déjà été tentée mais le fichier hôte ne peut supporter {payload_length} slots.")
                return

            print(f"!!! AUTO-CORRECTION DÉCLENCHÉE !!!")
            print(f"Nombre de points d'injection sûrs trouvés : {available_slots}. {payload_length} sont requis.")
            
            # Application du patch sur le contenu HTML
            html_content = auto_patch_html_slots(html_content, payload_length, available_slots)
            
            # Repasser à l'étape 4 pour rescanner les nouveaux index créés
            continue
        
        # Si les slots sont suffisants, sortir de la boucle d'auto-correction
        print(f"Nombre de points d'injection sûrs trouvés : {available_slots}.")
        break 

    # --- FIN BOUCLE D'AUTOCORRECTION/SCAN ---

    # 6. Phase de Sélection
    injection_slots = random.sample(safe_injection_indices, payload_length)
    injection_slots.sort() 
    
    print(f"Sélection de {payload_length} emplacements aléatoires pour l'injection...")
    
    # 7. Phase d'Injection (BF004, BF005)
    output_content = ""
    payload_char_index = 0
    slot_index = 0
    
    injection_functions = [creer_fauxcommentaire, creer_faussevariable]
    random.shuffle(injection_functions)
    
    for host_index in range(len(html_content)):
        
        output_content += html_content[host_index]
        
        if slot_index < len(injection_slots) and host_index + 1 == injection_slots[slot_index]:
            
            char_to_hide = encoded_payload[payload_char_index]
            injection_func = injection_functions[payload_char_index % len(injection_functions)]
            injected_code = injection_func(char_to_hide)
            
            output_content += injected_code
            
            print(f"    -> Injecte '{char_to_hide}' (Type: {injection_func.__name__}, Index Hote: {host_index + 1})")
            payload_char_index += 1
            slot_index += 1

    # 8. Finalisation
    if payload_char_index != payload_length:
        print("Erreur inattendue : Tous les caractères n'ont pas été insérés.")
    else:
        print("Tous les caracteres du payload ont ete inseres avec succes.")

    # 9. Ecriture du Fichier de Sortie
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Fichier steganographie cree : {OUTPUT_FILE}")
        print(f"L'encodage est complet et l'intégrité visuelle est préservée.")
    except Exception as e:
        print(f"Erreur lors de l'ecriture du fichier de sortie : {e}")

# ----------------------------------------------------
# Interface Utilisateur (Ligne de Commande) (3.3)
# ----------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Outil de Steganographie HTML. Encode le contenu d'un fichier payload dans un fichier HTML hôte.",
        epilog="Exemple: python encoder.py mapage.html payload.txt"
    )
    parser.add_argument(
        "html_source",
        help="Chemin vers le fichier HTML hôte à utiliser (e.g., mapage.html)."
    )
    parser.add_argument(
        "payload_source",
        help="Chemin vers le fichier contenant le payload à cacher (e.g., payload.txt)."
    )
    
    args = parser.parse_args()
    
    encode_html_steganography(args.html_source, args.payload_source)
