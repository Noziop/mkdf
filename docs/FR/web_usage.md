# Interface Web de MKDF

Ce guide explique comment utiliser l'interface web de MKDF pour créer visuellement des structures de répertoires et de fichiers.

## Démarrer l'interface web

Pour lancer l'interface web de MKDF, utilisez la commande suivante:

```bash
mkdf --web
# ou
mkdf -w
```

Par défaut, l'interface web est accessible à l'adresse http://localhost:8080

Vous pouvez spécifier un port différent en utilisant l'option `--port` ou `-p`:

```bash
mkdf --web --port 3000
# ou
mkdf -w -p 3000
```

## Navigation dans l'interface web

L'interface web de MKDF comporte plusieurs sections:

### Barre de navigation supérieure

- **Accueil**: Revenir à la page principale
- **Documentation**: Liens vers la documentation MKDF
- **Modèles**: Accéder aux modèles prédéfinis
- **À propos**: Informations sur le projet MKDF

### Panneau principal

L'interface principale est divisée en trois sections:

1. **Éditeur d'expression**: Zone où vous pouvez saisir votre expression MKDF
2. **Aperçu de la structure**: Visualisation en arborescence de la structure qui sera créée
3. **Options de configuration**: Paramètres supplémentaires pour la génération

## Utilisation de l'éditeur d'expression

L'éditeur d'expression vous permet de saisir une expression MKDF utilisant la même syntaxe que la version en ligne de commande:

1. Saisissez votre expression dans le champ de texte
   ```
   projet/{src/{models/,views/,controllers/},docs/,tests/}
   ```

2. Cliquez sur le bouton "Aperçu" pour visualiser la structure qui sera créée

3. L'aperçu se mettra à jour automatiquement et affichera une représentation arborescente de la structure

## Modes d'édition

L'interface web propose deux modes d'édition:

### Mode texte

Dans ce mode, vous saisissez directement l'expression MKDF comme vous le feriez en ligne de commande.

### Mode visuel

Le mode visuel vous permet de construire votre structure de répertoires et fichiers à l'aide d'une interface glisser-déposer:

1. Cliquez sur "Mode visuel" pour basculer vers l'éditeur graphique
2. Utilisez les boutons "Ajouter dossier" et "Ajouter fichier" pour créer votre structure
3. Faites glisser et déposez les éléments pour organiser votre arborescence
4. L'expression MKDF correspondante sera générée automatiquement

## Thèmes d'interface

MKDF propose différents thèmes visuels pour l'interface web:

1. **Clair**: Thème par défaut avec fond blanc
2. **Sombre**: Mode sombre pour une utilisation nocturne
3. **Girly**: Thème avec couleurs pastel et éléments arrondis
4. **Minimaliste**: Interface épurée avec le minimum d'éléments

Pour changer de thème:

1. Cliquez sur l'icône de thème dans le coin supérieur droit
2. Sélectionnez le thème de votre choix dans le menu déroulant

## Modèles prédéfinis

L'interface web vous permet d'utiliser les mêmes modèles prédéfinis que la version en ligne de commande:

1. Cliquez sur l'onglet "Modèles" dans la barre de navigation
2. Sélectionnez un modèle dans la liste:
   - Simple
   - Multi
   - Docker
   - FastAPI
   - Vue-Vite
   - Flask
   - React

3. Un aperçu de la structure du modèle s'affichera
4. Cliquez sur "Utiliser ce modèle" pour l'appliquer

## Personnalisation des modèles

Vous pouvez personnaliser un modèle après l'avoir sélectionné:

1. Sélectionnez un modèle dans la liste
2. Cliquez sur "Personnaliser"
3. Modifiez la structure dans l'éditeur visuel ou texte
4. Cliquez sur "Appliquer les modifications"

## Options de génération

L'interface web propose plusieurs options pour la génération de votre structure:

### Emplacement de génération

Par défaut, la structure est générée dans le répertoire courant, mais vous pouvez spécifier un chemin absolu ou relatif:

1. Dans la section "Options de configuration", saisissez le chemin dans le champ "Emplacement"
2. Vous pouvez également cliquer sur "Parcourir" pour sélectionner un emplacement

### Options avancées

- **Mode verbeux**: Affiche des détails sur chaque opération
- **Mode simulation**: Montre ce qui serait créé sans réellement le faire
- **Forcer la création**: Écrase les fichiers/dossiers existants
- **Ignorer les erreurs**: Continue la création même en cas d'erreur

## Exportation et importation

Vous pouvez sauvegarder et partager vos structures:

### Exportation

1. Créez votre structure dans l'éditeur
2. Cliquez sur "Exporter" dans le menu d'options
3. Choisissez le format d'exportation:
   - JSON
   - YAML
   - Expression MKDF
   - Script shell

### Importation

1. Cliquez sur "Importer" dans le menu d'options
2. Sélectionnez un fichier précédemment exporté
3. La structure sera chargée dans l'éditeur

## Génération de la structure

Une fois que vous êtes satisfait de votre structure:

1. Vérifiez l'aperçu pour vous assurer qu'il correspond à vos attentes
2. Configurez les options comme souhaité
3. Cliquez sur le bouton "Générer" pour créer la structure
4. Une notification vous indiquera si la génération a réussi ou échoué

## Terminal web

L'interface web propose un terminal intégré pour des opérations avancées:

1. Cliquez sur l'onglet "Terminal" dans le panneau inférieur
2. Vous pouvez y exécuter des commandes MKDF directement
3. Le terminal affiche également les logs de génération

## API Web

MKDF expose également une API REST que vous pouvez utiliser pour automatiser la création de structures:

```
POST /api/generate
{
  "expression": "projet/{src/,docs/,tests/}",
  "options": {
    "verbose": true,
    "force": false
  }
}
```

Consultez la documentation de l'API dans la section "API" du menu principal pour plus de détails.

## Résolution des problèmes

### La structure ne se génère pas

- Vérifiez que vous avez les droits d'écriture sur l'emplacement cible
- Assurez-vous que la syntaxe de votre expression est correcte
- Consultez les logs dans l'onglet "Terminal"

### L'interface web ne démarre pas

- Vérifiez que le port spécifié n'est pas déjà utilisé
- Assurez-vous que vous avez les droits pour lier le port
- Consultez les logs de démarrage

### L'aperçu ne se met pas à jour

- Vérifiez que votre expression MKDF est valide
- Essayez de rafraîchir la page
- Passez en mode texte puis revenez au mode visuel

## Raccourcis clavier

L'interface web de MKDF propose plusieurs raccourcis clavier pour accélérer votre flux de travail:

- `Ctrl+Enter`: Générer la structure
- `Ctrl+P`: Afficher l'aperçu
- `Ctrl+S`: Exporter la structure
- `Ctrl+O`: Importer une structure
- `Ctrl+/`: Basculer entre mode texte et mode visuel
- `Ctrl+H`: Afficher l'aide des raccourcis clavier

---

## Navigation

- [Retour à l'index](index.md)
- Pages connexes :
  - [Utilisation en ligne de commande](cli_usage.md)
  - [Modèles de projets](project_templates.md)
- [Guide du développeur](developer_guide.md)