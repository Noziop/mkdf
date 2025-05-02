# MKDF - MaKeDir&Files

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-AGPL--3.0-green.svg)

Un outil puissant pour créer rapidement des structures de répertoires et de fichiers à partir d'expressions simplifiées.

> **⚠️ Note aux développeurs :** La compilation du projet génère actuellement plusieurs warnings, principalement liés à la troncation potentielle de chaînes et à des comparaisons entre types signés et non signés. Ces warnings n'affectent pas le fonctionnement du programme mais nous cherchons des contributeurs pour nous aider à les résoudre. Voir la section [Contribution](#contribution) pour plus de détails.

## Présentation

MKDF (MaKeDir&Files) combine les fonctionnalités de `mkdir -p` et `touch` en un seul outil, avec en plus la puissance des expansions d'accolades. Il permet de créer rapidement des structures complexes de répertoires et de fichiers à partir d'une seule commande.

## Caractéristiques

- 🚀 Interface en ligne de commande (CLI) intuitive
- 💻 Interface web conviviale avec prévisualisation de la structure
- 🔧 Création de structures de fichiers avec expansion d'accolades
- 📄 Templates de fichiers pour créer des fichiers pré-remplis
- 📦 Modèles de projets prédéfinis (React, Flask, FastAPI, Vue+Vite, etc.)
- 🛠️ Structures personnalisées avec syntaxe expressive
- 🏠 Support pour l'expansion du tilde (~) dans les chemins
- ⚙️ Configuration personnalisable via ~/.config/mkdf/config

## Installation

Pour les instructions d'installation complètes, consultez le [Guide d'installation](docs/FR/installation.md).

### Depuis les sources

```bash
git clone https://github.com/Noziop/mkdf.git
cd mkdf
./install.sh       # Installation en français (par défaut)
./install.sh --EN  # Installation en anglais
```

Le script d'installation vous permettra de choisir entre :
- Installation système (dans /usr/local/bin, nécessite sudo)
- Installation utilisateur (dans ~/.local/bin)
- Installation dans un répertoire personnalisé

## Utilisation

### Mode ligne de commande

```bash
# Aide et version
mkdf --help
mkdf --version

# Mode interactif
mkdf

# Créer une structure avec expansion d'accolades
mkdf 'myproject/{src/{lib/,bin/,include/},docs/{user/,dev/},tests/,README.md,LICENSE}'

# Créer un projet à partir d'un modèle
mkdf --create my-project react
mkdf -c ~/projects/api-server fastapi

# Créer des fichiers à partir de templates
mkdf 'projet/{README.md:/chemin/vers/template.md,config.json:/chemin/vers/config.json}'

# Configuration
mkdf --config    # Configure l'application
```

Pour une documentation complète de l'interface en ligne de commande, consultez le [Guide d'utilisation CLI](docs/FR/cli_usage.md).

### Mode web

```bash
# Démarrer l'interface web
mkdf --web
# ou
make web
```

Puis ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8080).

Pour en savoir plus sur l'interface web, consultez le [Guide d'utilisation Web](docs/FR/web_usage.md).

## Syntaxe d'expansion

MKDF utilise une syntaxe d'expansion avec des accolades pour définir efficacement des structures complexes :

- `{a,b,c}` crée a, b et c au même niveau
- Les chemins terminés par `/` sont créés comme des répertoires
- Les autres sont créés comme des fichiers vides
- Vous pouvez imbriquer les accolades : `{a/{b,c},d}` crée a/b, a/c et d
- Pour utiliser un template : `fichier.txt:/chemin/vers/template.txt` crée fichier.txt avec le contenu du template

## Configuration

MKDF peut être configuré via un fichier de configuration situé dans `~/.config/mkdf/config`. Ce fichier est créé automatiquement lors de la première utilisation ou lors de l'installation.

### Options de configuration

Le fichier de configuration contient les paramètres suivants :

```
# Chemin vers les fichiers web
WEB_ROOT=/chemin/vers/repertoire/web

# Port du serveur web
WEB_PORT=8080

# Mode debug (0=désactivé, 1=activé)
DEBUG_MODE=0

# Répertoire des templates
TEMPLATE_DIR=/chemin/vers/repertoire/templates

# Paramètre régional
LOCALE=fr_FR
```

### Modifier la configuration

Vous pouvez modifier la configuration de deux façons :
1. En éditant directement le fichier `~/.config/mkdf/config`
2. En utilisant la commande `mkdf --config` qui ouvre le fichier de configuration dans votre éditeur par défaut

## Documentation complète

Toute la documentation est disponible en français et en anglais :

### Documentation Française

- [Index de la documentation](docs/FR/index.md)
- [Guide d'installation](docs/FR/installation.md)
- [Utilisation en ligne de commande](docs/FR/cli_usage.md)
- [Interface Web](docs/FR/web_usage.md)
- [Modèles de projets](docs/FR/project_templates.md)
- [Cas d'utilisation](docs/FR/use_cases.md)
- [Guide du développeur](docs/FR/developer_guide.md)

### English Documentation

- [Documentation Index](docs/EN/index.md)
- [Installation Guide](docs/EN/installation.md)
- [Command Line Usage](docs/EN/cli_usage.md)
- [Web Interface](docs/EN/web_usage.md)
- [Project Templates](docs/EN/project_templates.md)
- [Use Cases](docs/EN/use_cases.md)
- [Developer Guide](docs/EN/developer_guide.md)

## Licence

Ce projet est sous licence GNU Affero General Public License v3.0 (AGPL-3.0) - voir le fichier LICENSE pour plus de détails.

Cette licence libre garantit que :
1. Le code reste libre et open source
2. Toutes les modifications doivent également être partagées sous la même licence
3. Même lorsque le logiciel est proposé comme service réseau, le code source doit être rendu disponible
4. L'exploitation commerciale est soumise aux conditions de l'AGPL

## Auteur

Développé par [Fassih Belmokhtar](https://github.com/Noziop)  
Contact: contact@fassih.ch

## Contribution

Nous recherchons activement des contributeurs pour nous aider à améliorer MKDF, notamment pour résoudre les warnings de compilation actuels :

### Warnings actuels

```
gcc -Wall -Wextra -g -pthread -Iinclude -c src/cli_handler.c -o build/cli_handler.o
src/cli_handler.c: In function 'start_cli_mode':
src/cli_handler.c:993:58: warning: '%s' directive output may be truncated writing up to 4095 bytes into a region of size between 0 and 4095 [-Wformat-truncation=]
  993 |                         snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                                                          ^~                ~~~~~~~~~~
src/cli_handler.c:993:25: note: 'snprintf' output between 2 and 8192 bytes into a destination of size 4096
  993 |                         snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/cli_handler.c:918:70: warning: '%s' directive output may be truncated writing up to 4095 bytes into a region of size between 0 and 4095 [-Wformat-truncation=]
  918 |                                     snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                                                                      ^~                ~~~~~~~~~~
src/cli_handler.c:918:37: note: 'snprintf' output between 2 and 8192 bytes into a destination of size 4096
  918 |                                     snprintf(temp, sizeof(temp), "%s/%s", current_dir, target_dir);
      |                                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
src/cli_handler.c:957:78: warning: '%s' directive output may be truncated writing up to 1023 bytes into a region of size between 0 and 4095 [-Wformat-truncation=]
  957 |                             snprintf(project_path, sizeof(project_path), "%s/%s", target_dir, project_name);
      |                                                                              ^~               ~~~~~~~~~~~~
src/cli_handler.c:957:29: note: 'snprintf' output between 2 and 5120 bytes into a destination of size 4096
  957 |                             snprintf(project_path, sizeof(project_path), "%s/%s", target_dir, project_name);
      |                             ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At top level:
src/cli_handler.c:1289:12: warning: 'handle_directory_change' defined but not used [-Wunused-function]
 1289 | static int handle_directory_change(char *current_dir, size_t current_dir_size __attribute__((unused)), char *target_dir, size_t target_dir_size) {
      |            ^~~~~~~~~~~~~~~~~~~~~~~
gcc -Wall -Wextra -g -pthread -Iinclude -c src/web_handler.c -o build/web_handler.o
src/web_handler.c: In function 'handle_client':
src/web_handler.c:189:23: warning: comparison of integer expressions of different signedness: 'ssize_t' {aka 'long int'} and 'size_t' {aka 'long unsigned int'} [-Wsign-compare]
  189 |     while (total_sent < response_len) {
      |                       ^
```

### Comment contribuer

Si vous avez des compétences en C et souhaitez nous aider à améliorer MKDF :

1. **Résoudre les warnings de compilation** : Proposez des correctifs pour les warnings listés ci-dessus.
2. **Internationalisation** : Aidez-nous à mettre en place une meilleure structure pour la gestion multilingue.
3. **Amélioration du code** : Identifiez et corrigez les problèmes potentiels ou proposez des améliorations.

Pour contribuer :
1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b fix-warnings`)
3. Committez vos changements (`git commit -am 'Fix format truncation warnings'`)
4. Push la branche (`git push origin fix-warnings`)
5. Ouvrez une Pull Request

Nous sommes également ouverts à toute suggestion pour améliorer le projet !