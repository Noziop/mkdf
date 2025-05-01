# Documentation MKDF

Bienvenue dans la documentation de MKDF (MaKeDir&Files), un outil puissant pour créer des structures de répertoires et de fichiers.

## Table des matières

- [Guide d'installation](installation.md) - Comment installer MKDF sur votre système
- [Utilisation en ligne de commande](cli_usage.md) - Guide complet des commandes et options CLI
- [Interface Web](web_usage.md) - Comment utiliser l'interface web de MKDF
- [Modèles de projets](project_templates.md) - Les modèles prédéfinis disponibles
- [Cas d'utilisation](use_cases.md) - Exemples pratiques d'utilisation
- [Guide du développeur](developer_guide.md) - Documentation technique pour les contributeurs

## Qu'est-ce que MKDF ?

MKDF est un utilitaire flexible permettant de générer rapidement des structures de projets en utilisant une syntaxe d'expansion concise. Il propose :

- Une interface en ligne de commande intuitive
- Une interface web conviviale
- Une syntaxe puissante d'expansion d'accolades
- Des modèles prédéfinis pour différents types de projets
- Le support des chemins relatifs et absolus

## Débuter avec MKDF

Pour commencer à utiliser MKDF :

1. Consultez le [Guide d'installation](installation.md) pour installer l'outil
2. Explorez la [documentation d'utilisation en ligne de commande](cli_usage.md) ou l'[interface web](web_usage.md)
3. Découvrez les [cas d'utilisation](use_cases.md) pour des exemples concrets

## Exemples rapides

Créer une structure simple :
```bash
mkdf 'mon-projet/{src/,docs/,tests/}'
```

Utiliser un modèle prédéfini :
```bash
mkdf -c mon-app react
```

Lancer l'interface web :
```bash
mkdf --web
```