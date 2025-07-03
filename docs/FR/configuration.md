# Configuration de MKDF

MKDF offre plusieurs options de configuration pour personnaliser son comportement selon vos besoins. Cette page documente toutes les options disponibles et comment les modifier.

## Emplacement du fichier de configuration

Le fichier de configuration de MKDF est situé à l'emplacement suivant :

```
~/.config/mkdf/config
```

Ce fichier est automatiquement créé :
- Lors de la première utilisation de MKDF
- Lors de l'installation via le script `install.sh`
- Lorsque vous exécutez la commande `mkdf --config` si le fichier n'existe pas

## Structure du fichier de configuration

Le fichier de configuration utilise un format simple de paires clé-valeur :

```
# Commentaire
CLÉ=valeur
```

## Options disponibles

Le fichier de configuration contient les paramètres suivants :

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|------------------|
| `WEB_ROOT` | Chemin vers les fichiers web | Détecté automatiquement |
| `WEB_PORT` | Port du serveur web | 8080 |
| `DEBUG_MODE` | Mode debug (0=désactivé, 1=activé) | 0 |
| `TEMPLATE_DIR` | Répertoire des templates | Détecté automatiquement |
| `LOCALE` | Paramètre régional | fr_FR |

### WEB_ROOT

Chemin où sont stockés les fichiers statiques (HTML, CSS, JS) de l'interface web.

```
WEB_ROOT=/chemin/vers/repertoire/web
```

Par défaut, MKDF tente de détecter automatiquement ce chemin en fonction de l'emplacement de l'exécutable. Si vous avez déplacé les fichiers web, vous devrez mettre à jour cette valeur.

### WEB_PORT

Port sur lequel le serveur web de MKDF écoute.

```
WEB_PORT=8080
```

Si le port 8080 est déjà utilisé, vous pouvez spécifier un autre port.

### DEBUG_MODE

Active ou désactive le mode débogage. En mode débogage, des informations supplémentaires sont affichées dans la console.

```
DEBUG_MODE=0  # Mode normal
DEBUG_MODE=1  # Mode débogage
```

### TEMPLATE_DIR

Répertoire où sont stockés les templates utilisés pour la création de fichiers.

```
TEMPLATE_DIR=/chemin/vers/repertoire/templates
```

Par défaut, MKDF essaie de détecter automatiquement ce chemin.

### LOCALE

Paramètre régional à utiliser pour l'interface utilisateur.

```
LOCALE=fr_FR  # Français
LOCALE=en_US  # Anglais
```

## Modifier la configuration

Vous pouvez modifier la configuration de deux façons :

### 1. En utilisant la commande `mkdf --config`

Cette commande ouvre le fichier de configuration dans votre éditeur par défaut :

```bash
mkdf --config
# ou
mkdf --configure
```

Si le fichier de configuration n'existe pas, il sera créé avec des valeurs par défaut avant d'être ouvert.

### 2. En modifiant directement le fichier

Vous pouvez également modifier directement le fichier avec n'importe quel éditeur de texte :

```bash
# Avec nano
nano ~/.config/mkdf/config

# Avec vim
vim ~/.config/mkdf/config

# Avec VS Code
code ~/.config/mkdf/config
```

## Rétablir la configuration par défaut

Si vous souhaitez réinitialiser la configuration à ses valeurs par défaut, supprimez simplement le fichier de configuration et exécutez la commande `mkdf --config` :

```bash
rm ~/.config/mkdf/config
mkdf --config
```

## Variables d'environnement

Vous pouvez également influencer certains paramètres via des variables d'environnement :

| Variable | Correspond à | Priorité |
|----------|--------------|----------|
| `MKDF_WEB_ROOT` | `WEB_ROOT` | Plus haute que le fichier de config |

Exemple d'utilisation d'une variable d'environnement :

```bash
MKDF_WEB_ROOT=/mon/chemin/web mkdf --web
```