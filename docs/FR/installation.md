# Guide d'installation de MKDF

Ce guide vous explique comment installer MKDF sur votre système.

## Prérequis

Pour installer et utiliser MKDF, vous aurez besoin de :

- Un système Linux, macOS ou Windows avec WSL
- GCC ou Clang
- Make
- Bibliothèque pthread (généralement déjà installée sur la plupart des systèmes)

## Installation depuis les sources

### 1. Cloner le dépôt

```bash
git clone https://github.com/username/mkdf.git
cd mkdf
```

### 2. Compiler

```bash
make
```

### 3. Installer

Pour une installation système (nécessite les permissions administrateur) :

```bash
sudo make install
```

Par défaut, cela installera le binaire dans `/usr/local/bin`.

Pour une installation locale (dans votre répertoire personnel) :

```bash
make install PREFIX=~/.local
```

Assurez-vous que `~/.local/bin` est dans votre PATH :

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Vérifier l'installation

Pour vérifier que MKDF a été correctement installé :

```bash
mkdf --version
```

Cela devrait afficher le numéro de version de MKDF.

## Installation avec des options personnalisées

Vous pouvez personnaliser l'installation avec différentes options du Makefile :

```bash
# Compilation avec optimisations
make CFLAGS="-O2 -Wall -Wextra -pthread"

# Installation dans un répertoire spécifique
make install PREFIX=/opt/mkdf
```

## Désinstallation

Pour désinstaller MKDF :

```bash
# Si installé avec sudo make install
sudo make uninstall

# Si installé localement
make uninstall PREFIX=~/.local
```

## Configuration après installation

Après avoir installé MKDF, vous pouvez créer un fichier de configuration optionnel dans votre répertoire personnel :

```bash
mkdir -p ~/.config/mkdf
```

Vous pouvez créer un fichier `~/.config/mkdf/config.ini` avec le contenu suivant :

```ini
[general]
default_dir=~/projects

[templates]
custom_template_dir=~/.config/mkdf/templates

[web]
port=8080
```

## Résolution des problèmes courants

### Problème : Commande introuvable

Si vous obtenez une erreur "commande introuvable" après l'installation :

1. Vérifiez que le répertoire d'installation est dans votre PATH
2. Essayez de relancer votre terminal
3. Vérifiez les permissions du fichier binaire

### Problème : Erreurs de compilation

Si vous rencontrez des erreurs lors de la compilation :

1. Assurez-vous que vous avez toutes les dépendances nécessaires
2. Vérifiez que vous utilisez une version récente de GCC ou Clang
3. Sur certaines distributions Linux, vous pourriez avoir besoin d'installer le paquet `build-essential`

```bash
# Sur Debian/Ubuntu
sudo apt install build-essential

# Sur Fedora
sudo dnf install gcc make
```

### Problème : Erreurs à l'exécution

Si vous rencontrez des erreurs à l'exécution :

1. Vérifiez que vous avez les permissions nécessaires sur les répertoires où vous essayez de créer des fichiers
2. Assurez-vous que le système a suffisamment d'espace disque
3. En cas d'erreur liée à pthread, vérifiez que la bibliothèque est correctement installée

## Mise à jour

Pour mettre à jour MKDF vers la dernière version :

```bash
cd mkdf
git pull
make clean
make
sudo make install  # ou make install PREFIX=~/.local pour une installation locale
```

---

## Navigation

- [Retour à l'index](index.md)
- Page suivante : [Utilisation en ligne de commande](cli_usage.md)
- [Interface Web](web_usage.md)