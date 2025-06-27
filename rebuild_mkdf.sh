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

# Étape 5: Test rapide
echo
log_info "Step 5: Quick test..."
if mkdf create --help > /dev/null 2>&1; then
    log_info "MKDF successfully installed and working!"
    echo
    echo "🎉 Ready to test your changes!"
    echo "Try: mkdf create"
else
    log_error "MKDF installation verification failed!"
    exit 1
fi

echo
echo "=================================="
echo "🚀 MKDF rebuild complete!"
echo "You can now use MKDF with your latest changes."