#!/bin/bash

# rebuild_mkdf.sh - Automatise la réinstallation de MKDF après modifications

set -e  # Arrêt immédiat en cas d'erreur

echo "🔄 MKDF Rebuild & Reinstall Script"
echo "=================================="

# Couleurs pour le feedback
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction de log avec couleurs
log_info() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Étape 0: Vérifier si le server web est en cours d'exécution
echo
log_info "Step 0: Checking if web server is running..."
if mkdf web status > /dev/null 2>&1; then
    log_info "Web server is running."
    echo "Stopping the web server..."
    if mkdf web stop; then
        log_info "Web server stopped successfully."
    else
        log_error "Failed to stop the web server."
        exit 1
    fi
else
    log_warning "Web server is not running."
fi

# Étape 1: Désinstaller l'ancienne version
echo
log_info "Step 1: Uninstalling existing MKDF..."
if pip show mkdf > /dev/null 2>&1; then
    pip uninstall mkdf -y
    log_info "MKDF uninstalled successfully"
else
    log_warning "MKDF not currently installed"
fi

# Étape 2: Build avec Poetry
echo
log_info "Step 2: Building with Poetry..."
if ! poetry build; then
    log_error "Poetry build failed!"
    exit 1
fi

# Étape 3: Trouver le wheel le plus récent
echo
log_info "Step 3: Finding latest wheel..."
WHEEL_FILE=$(ls -t dist/mkdf-*.whl 2>/dev/null | head -n1)

if [ -z "$WHEEL_FILE" ]; then
    log_error "No wheel file found in dist/ directory!"
    exit 1
fi

log_info "Found wheel: $WHEEL_FILE"

# Étape 4: Installer le nouveau wheel
echo
log_info "Step 4: Installing new MKDF..."
if ! pip install "$WHEEL_FILE"; then
    log_error "Installation failed!"
    exit 1
fi

# Add ~/.local/bin to PATH for the quick test
export PATH="$HOME/.local/bin:$PATH"

# Étape 5: Test rapide
echo
log_info "Step 5: Quick test..."
if mkdf --help > /dev/null 2>&1; then
    log_info "MKDF successfully installed and working!"
    echo
    echo "🎉 Ready to test your changes!"
    echo "Try: mkdf create"
else
    log_error "MKDF installation verification failed!"
    exit 1
fi

# Étape 6: Relancer le serveur web
echo
log_info "do you want to restart the web server? (y/n)"
read -r RESTART_WEB
if [[ "$RESTART_WEB" == "y" ]]; then
    log_info "Step 6: Restarting web server..."
    if mkdf web start; then
        log_info "Web server started successfully."
    else
        log_error "Failed to start the web server."
    fi
    exit 1
fi

echo
echo "=================================="
echo "🚀 MKDF rebuild complete!"
echo "You can now use MKDF with your latest changes."