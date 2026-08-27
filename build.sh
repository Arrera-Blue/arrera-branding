#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPEC_FILE="$(find "${ROOT_DIR}" -maxdepth 1 -name "*.spec" | head -n 1)"
PACKAGE_NAME="$(grep -E '^Name:' "${SPEC_FILE}" | awk '{print $2}')"
VERSION="$(grep -E '^Version:' "${SPEC_FILE}" | awk '{print $2}')"
TARBALL_NAME="${PACKAGE_NAME}-${VERSION}"
BUILD_DIR="${ROOT_DIR}/build_rpm"
OUTPUT_DIR="${ROOT_DIR}/output"

echo "==> Préparation de la construction de ${PACKAGE_NAME}-${VERSION}..."

# Nettoyage
rm -rf "${BUILD_DIR}" "${OUTPUT_DIR}" "${TARBALL_NAME}.tar.gz"
mkdir -p "${BUILD_DIR}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS} "${OUTPUT_DIR}"

# Création de l'archive source tar.gz
echo "==> Création de l'archive source tar.gz..."
TMP_ARCHIVE_DIR=$(mktemp -d)
mkdir -p "${TMP_ARCHIVE_DIR}/${TARBALL_NAME}"

cp -r "${ROOT_DIR}/src" "${TMP_ARCHIVE_DIR}/${TARBALL_NAME}/"
cp "${ROOT_DIR}/LICENSE" "${TMP_ARCHIVE_DIR}/${TARBALL_NAME}/"
cp "${ROOT_DIR}/arrera-branding.spec" "${TMP_ARCHIVE_DIR}/${TARBALL_NAME}/"

tar -czf "${BUILD_DIR}/SOURCES/${TARBALL_NAME}.tar.gz" -C "${TMP_ARCHIVE_DIR}" "${TARBALL_NAME}"
rm -rf "${TMP_ARCHIVE_DIR}"

# Copie du spec file
cp "${ROOT_DIR}/arrera-branding.spec" "${BUILD_DIR}/SPECS/"

# Construction RPM et SRPM
echo "==> Lancement de rpmbuild..."
rpmbuild -ba \
    --define "_topdir ${BUILD_DIR}" \
    "${BUILD_DIR}/SPECS/arrera-branding.spec"

# Récupération des RPMs générés dans output/
find "${BUILD_DIR}/RPMS" -name "*.rpm" -exec cp {} "${OUTPUT_DIR}/" \;
find "${BUILD_DIR}/SRPMS" -name "*.rpm" -exec cp {} "${OUTPUT_DIR}/" \;

echo "==> Nettoyage du dossier temporaire de build..."
rm -rf "${BUILD_DIR}"

echo ""
echo "=========================================================="
echo " [SUCCÈS] RPMs générés dans : ${OUTPUT_DIR}"
echo "=========================================================="
ls -lh "${OUTPUT_DIR}"
