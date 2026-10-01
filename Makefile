# ==============================================================================
# Makefile pour arrera-branding
# Arrera Linux - Multi-Edition Visual Assets & Branding
# ==============================================================================

NAME        := arrera-branding
RPM_DIR     := rpm
EDITIONS    := home education enterprise server
VERSION     ?= $(shell awk '/^Version:/ {print $$2; exit}' $(RPM_DIR)/arrera-branding-home.spec)
PREFIX      ?= /usr
SYSCONFDIR  ?= /etc
DATADIR     ?= $(PREFIX)/share
LIBEXECDIR  ?= $(PREFIX)/libexec
UNITDIR     ?= $(PREFIX)/lib/systemd/system

BUILD_DIR   := build_rpm
OUTPUT_DIR  ?= output
TARBALL     := $(NAME)-$(VERSION).tar.gz

.PHONY: all help test install dist srpm rpm clean $(EDITIONS)

all: help

help:
	@echo "Cibles disponibles pour $(NAME) v$(VERSION) :"
	@echo "  make test      - Valide la syntaxe des scripts Shell et des specs"
	@echo "  make dist      - Génère l'archive tarball source ($(TARBALL))"
	@echo "  make srpm      - Génère les 4 paquets sources SRPM pour Fedora / COPR"
	@echo "  make rpm       - Construit les 4 paquets binaires RPM noarch dans output/"
	@echo "  make clean     - Nettoie les répertoires et fichiers de construction"

test:
	@echo "=== [1/2] Validation syntaxique des scripts Shell ==="
	@bash -n common/scripts/99-arrera-title.install
	@bash -n common/scripts/arrera-branding-guard.sh
	@bash -n build.sh
	@echo "-> Scripts Shell valides."
	@echo "=== [2/2] Validation des fichiers RPM spec ==="
	@for ed in $(EDITIONS); do \
		echo "-> Vérification de $(RPM_DIR)/arrera-branding-$${ed}.spec..."; \
		if command -v rpmlint >/dev/null 2>&1; then \
			rpmlint $(RPM_DIR)/arrera-branding-$${ed}.spec || true; \
		fi; \
	done
	@echo "=== Tous les tests ont réussi ! ==="

dist: clean
	@echo "Création de l'archive $(TARBALL)..."
	@TMPDIR=$$(mktemp -d); \
	mkdir -p $${TMPDIR}/$(NAME)-$(VERSION); \
	cp -r common editions LICENSE $${TMPDIR}/$(NAME)-$(VERSION)/; \
	tar -czf $(TARBALL) -C $${TMPDIR} $(NAME)-$(VERSION); \
	rm -rf $${TMPDIR}; \
	echo "Archive créée : $(TARBALL)"

srpm: dist
	@echo "Génération des 4 paquets sources (SRPM)..."
	@mkdir -p $(BUILD_DIR)/{BUILD,RPMS,SOURCES,SPECS,SRPMS} $(OUTPUT_DIR)
	@cp $(TARBALL) $(BUILD_DIR)/SOURCES/
	@for ed in $(EDITIONS); do \
		echo "-> SRPM [$$ed]..."; \
		cp $(RPM_DIR)/arrera-branding-$${ed}.spec $(BUILD_DIR)/SPECS/; \
		rpmbuild -bs --define "_topdir $(CURDIR)/$(BUILD_DIR)" $(BUILD_DIR)/SPECS/arrera-branding-$${ed}.spec; \
	done
	@cp $(BUILD_DIR)/SRPMS/*.src.rpm $(OUTPUT_DIR)/
	@cp $(TARBALL) $(OUTPUT_DIR)/
	@echo "SRPMs générés dans $(OUTPUT_DIR)/"

rpm: dist
	@echo "Construction des 4 paquets binaires RPM noarch..."
	@mkdir -p $(BUILD_DIR)/{BUILD,RPMS,SOURCES,SPECS,SRPMS} $(OUTPUT_DIR)
	@cp $(TARBALL) $(BUILD_DIR)/SOURCES/
	@for ed in $(EDITIONS); do \
		echo "==> Construction RPM [$$ed]..."; \
		cp $(RPM_DIR)/arrera-branding-$${ed}.spec $(BUILD_DIR)/SPECS/; \
		rpmbuild -ba --define "_topdir $(CURDIR)/$(BUILD_DIR)" $(BUILD_DIR)/SPECS/arrera-branding-$${ed}.spec; \
	done
	@cp $(BUILD_DIR)/RPMS/noarch/*.rpm $(OUTPUT_DIR)/ || true
	@cp $(BUILD_DIR)/SRPMS/*.src.rpm $(OUTPUT_DIR)/ || true
	@cp $(TARBALL) $(OUTPUT_DIR)/
	@echo "Les 4 RPMs ont été générés avec succès dans $(OUTPUT_DIR)/"

clean:
	@rm -rf $(BUILD_DIR) $(OUTPUT_DIR) $(TARBALL) *.src.rpm *.noarch.rpm
	@echo "Nettoyage terminé."
