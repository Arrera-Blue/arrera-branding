# Arrera Branding (`arrera-branding`)

Paquets RPM fournissant l'identité visuelle, les logos et la personnalisation système pour les 4 éditions de la distribution **Arrera Linux** :
- 🏠 **Home** : Identité poste de travail familiale avec thème Plymouth Arrera
- 🎓 **Éducation** : Identité scolaire/éducative avec thème Plymouth Arrera
- 🏢 **Entreprise** : Identité professionnelle/corporate avec thème Plymouth Arrera
- 🖥️ **Serveur** : Identité serveur en mode texte natif (**sans Plymouth**)

Chaque édition produit un **paquet RPM autonome et indépendant** (`arrera-branding-home.rpm`, `arrera-branding-education.rpm`, etc.) qui fournit `arrera-branding` et est mutuellement exclusif (`Conflicts`) avec les autres éditions.

---

## 📁 Structure du projet

Pour éviter toute duplication de code, les composants sont scindés entre une base commune (`common/`) et les identités spécifiques (`editions/`) :

```text
arrera-branding/
├── common/                            # 🔄 Composants partagés (zéro duplication)
│   ├── pixmaps/                       # Logos Arrera (PNG/SVG) et bannières de couleur
│   ├── fastfetch/                     # Configuration Fastfetch & logo ASCII
│   ├── plymouth/                      # Thème splash boot Arrera
│   ├── gdm/                           # Configuration dconf & écran de login GDM
│   ├── scripts/
│   │   ├── 99-arrera-title.install       # Hook dynamique de titre GRUB/BLS pour kernel-install
│   │   └── arrera-branding-guard.sh      # Garde d'identité système après 'dnf upgrade'
│   └── systemd/
│       └── arrera-branding-guard.service
├── editions/                          # 🎯 Identités propres à chaque édition
│   ├── home/
│   │   ├── os-release
│   │   └── arrera-release
│   ├── education/
│   │   ├── os-release
│   │   └── arrera-release
│   ├── enterprise/
│   │   ├── os-release
│   │   └── arrera-release
│   └── server/                        # (Pas de Plymouth au packaging)
│       ├── os-release
│       └── arrera-release
├── rpm/                               # Spécifications RPM par édition
│   ├── arrera-branding-home.spec
│   ├── arrera-branding-education.spec
│   ├── arrera-branding-enterprise.spec
│   └── arrera-branding-server.spec
├── Makefile                           # Automatisation des tests et builds
├── build.sh                           # Script de construction multi-éditions
├── LICENSE
└── README.md
```

---

## 🚀 Construction des paquets RPM

Le script `build.sh` permet de compiler l'ensemble des 4 RPMs ou une édition en particulier :

### 1. Compiler les 4 éditions en une seule commande

```bash
./build.sh
```

Cette commande génère dans le dossier `output/` :
- `arrera-branding-home-*.noarch.rpm` & `*.src.rpm`
- `arrera-branding-education-*.noarch.rpm` & `*.src.rpm`
- `arrera-branding-enterprise-*.noarch.rpm` & `*.src.rpm`
- `arrera-branding-server-*.noarch.rpm` & `*.src.rpm`

### 2. Options de construction

```bash
# Compiler uniquement l'édition Serveur :
./build.sh --edition server

# Compiler uniquement l'édition Home :
./build.sh --edition home

# Générer uniquement les paquets sources (SRPM) pour Fedora COPR :
./build.sh --srpm

# Nettoyer les répertoires temporaires :
./build.sh --clean
```

---

## 📦 Installation sur un système Arrera

Chaque RPM est autonome et embarque à la fois les assets visuels partagés et sa configuration d'édition :

```bash
# Pour une station Home :
sudo dnf install -y output/arrera-branding-home-*.noarch.rpm

# Pour un serveur :
sudo dnf install -y output/arrera-branding-server-*.noarch.rpm
```
