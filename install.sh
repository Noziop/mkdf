#!/bin/bash
#
# Script d'installation pour MKDF
# Ce script compile et installe MKDF sur votre système.

# Définition des couleurs pour les messages
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# Traitement des arguments en ligne de commande
LANGUAGE="FR"  # Langue par défaut

# Parcourir les arguments
for arg in "$@"; do
    case $arg in
        --EN|--en|-EN|-en)
            LANGUAGE="EN"
            shift
            ;;
        --FR|--fr|-FR|-fr)
            LANGUAGE="FR"
            shift
            ;;
    esac
done

# Messages multilingues
if [ "$LANGUAGE" = "EN" ]; then
    # Messages en anglais
    MSG_WELCOME="MKDF - MaKeDir&Files\nInstallation Script"
    MSG_PREREQ_CHECK="Checking prerequisites..."
    MSG_GCC_FOUND="✓ GCC found"
    MSG_CLANG_FOUND="✓ Clang found"
    MSG_NO_COMPILER="✗ Neither GCC nor Clang is installed. Please install a C compiler."
    MSG_DEBIAN_COMPILER="Debian/Ubuntu: sudo apt install build-essential"
    MSG_FEDORA_COMPILER="Fedora: sudo dnf install gcc"
    MSG_ARCH_COMPILER="Arch: sudo pacman -S base-devel"
    MSG_MAKE_FOUND="✓ Make found"
    MSG_MAKE_MISSING="✗ Make is not installed. Please install make."
    MSG_DEBIAN_MAKE="Debian/Ubuntu: sudo apt install make"
    MSG_FEDORA_MAKE="Fedora: sudo dnf install make"
    MSG_ARCH_MAKE="Arch: sudo pacman -S base-devel"
    MSG_PTHREAD_CHECK="Checking for pthread... "
    MSG_PTHREAD_FOUND="✓ Pthread found"
    MSG_PTHREAD_MISSING="✗ Pthread is not available."
    MSG_DEBIAN_PTHREAD="Debian/Ubuntu: sudo apt install libpthread-stubs0-dev"
    MSG_FEDORA_PTHREAD="Fedora: pthread is included in glibc-devel"
    MSG_ARCH_PTHREAD="Arch: pthread is included in base-devel"
    MSG_INSTALL_TYPE="Choose installation type:"
    MSG_SYSTEM_INSTALL="1) System installation (requires sudo, installs to /usr/local/bin)"
    MSG_USER_INSTALL="2) User installation (installs to ~/.local/bin)"
    MSG_CUSTOM_INSTALL="3) Custom directory installation"
    MSG_CHOICE="Your choice [1-3] (default: 1): "
    MSG_CUSTOM_PATH="Enter installation path (example: /opt/mkdf): "
    MSG_INVALID_PATH="Invalid path. Installation cancelled."
    MSG_COMPILING="Compiling MKDF..."
    MSG_COMPILE_FAILED="Compilation failed. Please check the errors above."
    MSG_INSTALLING="Installing MKDF to $PREFIX/bin..."
    MSG_INSTALL_FAILED="Installation failed. Please check the errors above."
    MSG_INSTALL_SUCCESS="MKDF has been installed successfully!"
    MSG_CONFIG_DIR="Creating configuration directory..."
    MSG_PATH_WARNING="WARNING: $PREFIX/bin is not in your PATH."
    MSG_PATH_BASH="To add this directory to your PATH, run the following command:"
    MSG_PATH_ZSH="Or for zsh:"
    MSG_POST_INSTALL="=== Post-installation instructions ==="
    MSG_CHECK_INSTALL="To verify that MKDF is correctly installed, run:"
    MSG_CREATE_CONFIG="To create a default configuration, you can create a file:"
    MSG_THANKS="Thank you for installing MKDF!"
else
    # Messages en français (existants)
    MSG_WELCOME="MKDF - MaKeDir&Files\nScript d'installation"
    MSG_PREREQ_CHECK="Vérification des prérequis..."
    MSG_GCC_FOUND="✓ GCC trouvé"
    MSG_CLANG_FOUND="✓ Clang trouvé"
    MSG_NO_COMPILER="✗ Ni GCC ni Clang n'est installé. Veuillez installer un compilateur C."
    MSG_DEBIAN_COMPILER="Debian/Ubuntu: sudo apt install build-essential"
    MSG_FEDORA_COMPILER="Fedora: sudo dnf install gcc"
    MSG_ARCH_COMPILER="Arch: sudo pacman -S base-devel"
    MSG_MAKE_FOUND="✓ Make trouvé"
    MSG_MAKE_MISSING="✗ Make n'est pas installé. Veuillez installer make."
    MSG_DEBIAN_MAKE="Debian/Ubuntu: sudo apt install make"
    MSG_FEDORA_MAKE="Fedora: sudo dnf install make"
    MSG_ARCH_MAKE="Arch: sudo pacman -S base-devel"
    MSG_PTHREAD_CHECK="Vérification de pthread... "
    MSG_PTHREAD_FOUND="✓ Pthread trouvé"
    MSG_PTHREAD_MISSING="✗ Pthread n'est pas disponible."
    MSG_DEBIAN_PTHREAD="Debian/Ubuntu: sudo apt install libpthread-stubs0-dev"
    MSG_FEDORA_PTHREAD="Fedora: pthread est inclus dans glibc-devel"
    MSG_ARCH_PTHREAD="Arch: pthread est inclus dans base-devel"
    MSG_INSTALL_TYPE="Choisissez le type d'installation :"
    MSG_SYSTEM_INSTALL="1) Installation système (nécessite sudo, installé dans /usr/local/bin)"
    MSG_USER_INSTALL="2) Installation utilisateur (installé dans ~/.local/bin)"
    MSG_CUSTOM_INSTALL="3) Installation dans un répertoire personnalisé"
    MSG_CHOICE="Votre choix [1-3] (défaut: 1): "
    MSG_CUSTOM_PATH="Entrez le chemin d'installation (exemple: /opt/mkdf): "
    MSG_INVALID_PATH="Chemin invalide. Installation annulée."
    MSG_COMPILING="Compilation de MKDF..."
    MSG_COMPILE_FAILED="La compilation a échoué. Veuillez vérifier les erreurs ci-dessus."
    MSG_INSTALLING="Installation de MKDF dans $PREFIX/bin..."
    MSG_INSTALL_FAILED="L'installation a échoué. Veuillez vérifier les erreurs ci-dessus."
    MSG_INSTALL_SUCCESS="MKDF a été installé avec succès !"
    MSG_CONFIG_DIR="Création du répertoire de configuration..."
    MSG_PATH_WARNING="ATTENTION: $PREFIX/bin n'est pas dans votre PATH."
    MSG_PATH_BASH="Pour ajouter ce répertoire à votre PATH, exécutez la commande suivante :"
    MSG_PATH_ZSH="Ou pour zsh :"
    MSG_POST_INSTALL="=== Instructions post-installation ==="
    MSG_CHECK_INSTALL="Pour vérifier que MKDF est correctement installé, exécutez :"
    MSG_CREATE_CONFIG="Pour créer une configuration par défaut, vous pouvez créer un fichier :"
    MSG_THANKS="Merci d'avoir installé MKDF !"
fi

# Message de bienvenue
echo -e "${BLUE}"
echo "==============================================="
echo -e "      $(echo -e "$MSG_WELCOME")"
echo "==============================================="
echo -e "${NC}"

# Vérification des prérequis
echo -e "${YELLOW}$MSG_PREREQ_CHECK${NC}"

# Vérification de GCC/Clang
if command -v gcc >/dev/null 2>&1; then
    echo -e "${GREEN}$MSG_GCC_FOUND${NC}"
    COMPILER="gcc"
elif command -v clang >/dev/null 2>&1; then
    echo -e "${GREEN}$MSG_CLANG_FOUND${NC}"
    COMPILER="clang"
else
    echo -e "${RED}$MSG_NO_COMPILER${NC}"
    echo "  $MSG_DEBIAN_COMPILER"
    echo "  $MSG_FEDORA_COMPILER"
    echo "  $MSG_ARCH_COMPILER"
    exit 1
fi

# Vérification de Make
if command -v make >/dev/null 2>&1; then
    echo -e "${GREEN}$MSG_MAKE_FOUND${NC}"
else
    echo -e "${RED}$MSG_MAKE_MISSING${NC}"
    echo "  $MSG_DEBIAN_MAKE"
    echo "  $MSG_FEDORA_MAKE"
    echo "  $MSG_ARCH_MAKE"
    exit 1
fi

# Vérification de pthread
echo -n "$MSG_PTHREAD_CHECK"
cat > /tmp/pthread_test.c << EOF
#include <pthread.h>
int main() { pthread_t t; return 0; }
EOF

if $COMPILER -pthread /tmp/pthread_test.c -o /tmp/pthread_test >/dev/null 2>&1; then
    echo -e "${GREEN}$MSG_PTHREAD_FOUND${NC}"
else
    echo -e "${RED}$MSG_PTHREAD_MISSING${NC}"
    echo "  $MSG_DEBIAN_PTHREAD"
    echo "  $MSG_FEDORA_PTHREAD"
    echo "  $MSG_ARCH_PTHREAD"
    exit 1
fi
rm -f /tmp/pthread_test.c /tmp/pthread_test

# Demander le type d'installation
echo ""
echo -e "${BLUE}$MSG_INSTALL_TYPE${NC}"
echo "$MSG_SYSTEM_INSTALL"
echo "$MSG_USER_INSTALL"
echo "$MSG_CUSTOM_INSTALL"
echo -n "$MSG_CHOICE"
read -r INSTALL_TYPE

# Configuration des options d'installation
case $INSTALL_TYPE in
    2)
        PREFIX="$HOME/.local"
        NEED_SUDO=0
        ;;
    3)
        echo -n "$MSG_CUSTOM_PATH"
        read -r CUSTOM_PREFIX
        if [ -z "$CUSTOM_PREFIX" ]; then
            echo -e "${RED}$MSG_INVALID_PATH${NC}"
            exit 1
        fi
        PREFIX="$CUSTOM_PREFIX"
        
        # Vérifier si le chemin nécessite sudo
        if [ -w "$(dirname "$PREFIX")" ]; then
            NEED_SUDO=0
        else
            NEED_SUDO=1
        fi
        ;;
    *)
        # Option par défaut : installation système
        PREFIX="/usr/local"
        NEED_SUDO=1
        ;;
esac

echo ""
echo -e "${YELLOW}$MSG_COMPILING${NC}"
make clean
make

if [ $? -ne 0 ]; then
    echo -e "${RED}$MSG_COMPILE_FAILED${NC}"
    exit 1
fi

# Définir le man correcte en fonction de la langue
if [ "$LANGUAGE" = "EN" ]; then
    MAN_FILE="mkdf.en.1"
else
    MAN_FILE="mkdf.1"
fi

echo ""
echo -e "${YELLOW}$MSG_INSTALLING${NC}"

# Installation avec ou sans sudo selon les besoins
if [ $NEED_SUDO -eq 1 ]; then
    sudo make install PREFIX="$PREFIX" MAN_FILE="$MAN_FILE"
else
    make install PREFIX="$PREFIX" MAN_FILE="$MAN_FILE"
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}$MSG_INSTALL_FAILED${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}$MSG_INSTALL_SUCCESS${NC}"

# Création du répertoire de configuration
echo -e "${YELLOW}$MSG_CONFIG_DIR${NC}"
mkdir -p ~/.config/mkdf

# Si la langue est l'anglais, créer un fichier de configuration pour définir la langue
if [ "$LANGUAGE" = "EN" ]; then
    echo "language=en" > ~/.config/mkdf/config.ini
else
    echo "language=fr" > ~/.config/mkdf/config.ini
fi

# Vérifier si le répertoire bin de l'installation est dans le PATH
if [[ ":$PATH:" != *":$PREFIX/bin:"* ]] && [ $INSTALL_TYPE -eq 2 ]; then
    echo ""
    echo -e "${YELLOW}$MSG_PATH_WARNING${NC}"
    echo "$MSG_PATH_BASH"
    echo ""
    echo "echo 'export PATH=\"\$PATH:$PREFIX/bin\"' >> ~/.bashrc && source ~/.bashrc"
    echo ""
    echo "$MSG_PATH_ZSH"
    echo "echo 'export PATH=\"\$PATH:$PREFIX/bin\"' >> ~/.zshrc && source ~/.zshrc"
fi

# Instructions post-installation
echo ""
echo -e "${BLUE}=== $MSG_POST_INSTALL ===${NC}"
echo "$MSG_CHECK_INSTALL"
echo "  mkdf --version"
echo ""
echo "$MSG_CREATE_CONFIG"
echo "  ~/.config/mkdf/config.ini"
echo ""
echo "$MSG_THANKS"
echo -e "${BLUE}===============================================${NC}"