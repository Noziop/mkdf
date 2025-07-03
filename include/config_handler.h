#ifndef CONFIG_HANDLER_H
#define CONFIG_HANDLER_H

/**
 * Structure contenant les paramètres de configuration de MKDF
 */
typedef struct {
    char web_root_path[4096];    // Chemin vers les fichiers web
    int web_port;                // Port du serveur web
    int debug_mode;              // Mode debug (0=désactivé, 1=activé)
    char template_dir[4096];     // Répertoire des templates
    char locale[32];             // Paramètre régional (fr_FR, en_US, etc.)
    char author_name[256];       // Nom de l'auteur par défaut
    char default_template[64];   // Modèle de projet par défaut
    char default_css[64];        // Thème CSS par défaut
    char language[8];            // Langue de l'interface (fr, en)
    // Ajoutez ici d'autres paramètres selon vos besoins
} mkdf_config_t;

/**
 * Charge la configuration depuis le fichier ~/.config/mkdf/config
 * Si le fichier n'existe pas, crée une configuration par défaut
 *
 * @return Structure contenant la configuration chargée
 */
mkdf_config_t load_config(void);

/**
 * Sauvegarde la configuration dans le fichier ~/.config/mkdf/config
 *
 * @param config Structure contenant la configuration à sauvegarder
 * @return 0 en cas de succès, -1 sinon
 */
int save_config(const mkdf_config_t *config);

/**
 * Crée le fichier de configuration avec les valeurs par défaut
 * 
 * @return 0 en cas de succès, -1 sinon
 */
int create_default_config(void);

/**
 * Récupère le chemin complet du fichier de configuration
 * 
 * @param buffer Buffer où stocker le chemin
 * @param size Taille du buffer
 * @return 0 en cas de succès, -1 sinon
 */
int get_config_file_path(char *buffer, size_t size);

/**
 * Récupère la configuration globale
 * 
 * @return Pointeur vers la configuration globale
 */
mkdf_config_t *get_global_config(void);

/**
 * Initialise le système de configuration
 * Charge les paramètres depuis le fichier ou crée une configuration par défaut
 * 
 * @return 0 en cas de succès, -1 sinon
 */
int init_config(void);

#endif /* CONFIG_HANDLER_H */