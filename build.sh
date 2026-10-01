#!/usr/bin/bash
# ==============================================================================
# Arrera Linux - Script de construction multi-éditions pour arrera-branding
# Compile et génère les 4 paquets RPM autonomes dans output/ :
#   - arrera-branding-home-*.noarch.rpm
#   - arrera-branding-education-*.noarch.rpm
#   - arrera-branding-enterprise-*.noarch.rpm
#   - arrera-branding-server-*.noarch.rpm
# ==============================================================================

set -e

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

RPM_DIR="${ROOT_DIR}/rpm"
BUILD_DIR="${ROOT_DIR}/build_rpm"
OUTPUT_DIR="${ROOT_DIR}/output"
ALL_EDITIONS=("home" "education" "enterprise" "server")

# Détection de la version depuis les specs
VERSION_SPEC="$(find "${RPM_DIR}" -maxdepth 1 -name "arrera-branding-*.spec" | head -n 1)"
if [ -z "$VERSION_SPEC" ] || [ ! -f "$VERSION_SPEC" ]; then
    echo -e "${RED}Erreur: aucun fichier .spec trouvé dans ${RPM_DIR}/${NC}"
    exit 1
fi
VERSION="$(grep -E '^Version:' "${VERSION_SPEC}" | awk '{print $2}')"

echo -e "${BLUE}${BOLD}==========================================================${NC}"
echo -e "${CYAN}${BOLD}   Arrera Branding - Constructeur Multi-Éditions RPM      ${NC}"
echo -e "${CYAN}${BOLD}                 Version ${VERSION}                       ${NC}"
echo -e "${BLUE}${BOLD}==========================================================${NC}"

usage() {
    echo -e "${BOLD}Usage:${NC} $0 [OPTIONS]"
    echo ""
    echo -e "${BOLD}Options disponibles :${NC}"
    echo -e "  ${GREEN}(sans argument)${NC}      Compile les 4 éditions RPM + SRPM dans ${CYAN}${OUTPUT_DIR}/${NC}"
    echo -e "  ${GREEN}--edition <nom>${NC}      Compile uniquement l'édition spécifiée (${CYAN}home${NC}, ${CYAN}education${NC}, ${CYAN}enterprise${NC}, ${CYAN}server${NC})"
    echo -e "  ${GREEN}--srpm${NC}               Génère uniquement les paquets sources SRPM pour Fedora COPR"
    echo -e "  ${GREEN}--clean${NC}              Nettoie les dossiers temporaires de build et output/"
    echo -e "  ${GREEN}--help${NC}               Affiche cette aide"
    echo ""
}

# Nettoyage
clean_build() {
    echo -e "${YELLOW}--> Nettoyage des dossiers de build...${NC}"
    rm -rf "${BUILD_DIR}" "${OUTPUT_DIR}" *.tar.gz
    echo -e "${GREEN}✓ Nettoyage terminé.${NC}"
}

# Gestion des arguments
MODE="rpm"
TARGET_EDITIONS=("${ALL_EDITIONS[@]}")

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            usage
            exit 0
            ;;
        --clean|-c)
            clean_build
            exit 0
            ;;
        --srpm|-s)
            MODE="srpm"
            shift
            ;;
        --edition|-e)
            if [ -z "$2" ]; then
                echo -e "${RED}Erreur: --edition requiert un nom d'édition (home, education, enterprise, server).${NC}"
                exit 1
            fi
            TARGET_EDITIONS=("$2")
            shift 2
            ;;
        *)
            echo -e "${RED}Option inconnue : $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Vérification des outils nécessaires
for CMD in rpmbuild tar; do
    if ! command -v "$CMD" >/dev/null 2>&1; then
        echo -e "${RED}Erreur: la commande '$CMD' est requise mais introuvable.${NC}"
        echo -e "${YELLOW}Installez-la avec : sudo dnf install -y rpm-build${NC}"
        exit 1
    fi
done

# Nettoyage et initialisation de l'arborescence rpmbuild
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS} "${OUTPUT_DIR}"

# Préparation de l'archive source unique partagée
echo -e "${CYAN}--> Création de l'archive source arrera-branding-${VERSION}.tar.gz...${NC}"
TMP_ARCHIVE_DIR=$(mktemp -d)
mkdir -p "${TMP_ARCHIVE_DIR}/arrera-branding-${VERSION}"
cp -r "${ROOT_DIR}/common" "${TMP_ARCHIVE_DIR}/arrera-branding-${VERSION}/"
cp -r "${ROOT_DIR}/editions" "${TMP_ARCHIVE_DIR}/arrera-branding-${VERSION}/"
cp "${ROOT_DIR}/LICENSE" "${TMP_ARCHIVE_DIR}/arrera-branding-${VERSION}/"

tar -czf "${BUILD_DIR}/SOURCES/arrera-branding-${VERSION}.tar.gz" -C "${TMP_ARCHIVE_DIR}" "arrera-branding-${VERSION}"
rm -rf "${TMP_ARCHIVE_DIR}"

# Construction de chaque édition
for EDITION in "${TARGET_EDITIONS[@]}"; do
    SPEC_EDITION="${RPM_DIR}/arrera-branding-${EDITION}.spec"
    if [ ! -f "${SPEC_EDITION}" ]; then
        echo -e "${RED}Erreur: le fichier spec ${SPEC_EDITION} n'existe pas.${NC}"
        exit 1
    fi

    echo ""
    echo -e "${BOLD}${CYAN}==> Construction du paquet RPM pour l'édition [${EDITION}]...${NC}"
    cp "${SPEC_EDITION}" "${BUILD_DIR}/SPECS/"

    if [ "$MODE" = "srpm" ]; then
        rpmbuild -bs \
            --define "_topdir ${BUILD_DIR}" \
            "${BUILD_DIR}/SPECS/arrera-branding-${EDITION}.spec"
    else
        rpmbuild -ba \
            --define "_topdir ${BUILD_DIR}" \
            "${BUILD_DIR}/SPECS/arrera-branding-${EDITION}.spec"
    fi
done

# Déplacement des RPMs et SRPMs vers output/
echo ""
echo -e "${CYAN}--> Déplacement des RPMs générés dans ${OUTPUT_DIR}/...${NC}"
find "${BUILD_DIR}/RPMS" -name "*.rpm" -exec cp {} "${OUTPUT_DIR}/" \; 2>/dev/null || true
find "${BUILD_DIR}/SRPMS" -name "*.rpm" -exec cp {} "${OUTPUT_DIR}/" \; 2>/dev/null || true
rm -rf "${BUILD_DIR}"

echo ""
echo -e "${GREEN}${BOLD}==========================================================${NC}"
echo -e "${GREEN}${BOLD}       Compilation terminée avec succès !                 ${NC}"
echo -e "${GREEN}${BOLD}==========================================================${NC}"
echo -e "${BOLD}Paquets RPM générés dans le dossier ${CYAN}${OUTPUT_DIR}/${NC} :${BOLD}"
ls -lh "${OUTPUT_DIR}" | awk 'NR>1 {print "  - " $9 " (" $5 ")"}'

echo ""
echo -e "${YELLOW}Pour installer une édition sur un système cible :${NC}"
echo -e "  ${BOLD}sudo dnf install -y ${OUTPUT_DIR}/arrera-branding-home-*.noarch.rpm${NC}"
echo -e "  ${BOLD}sudo dnf install -y ${OUTPUT_DIR}/arrera-branding-education-*.noarch.rpm${NC}"
echo -e "  ${BOLD}sudo dnf install -y ${OUTPUT_DIR}/arrera-branding-enterprise-*.noarch.rpm${NC}"
echo -e "  ${BOLD}sudo dnf install -y ${OUTPUT_DIR}/arrera-branding-server-*.noarch.rpm${NC}"
echo ""
