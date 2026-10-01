# Arrera Branding

Paquet RPM `arrera-branding` fournissant l'identité visuelle et les logos pour la distribution **Arrera Linux** (GNOME, GDM, Plymouth, Fastfetch, OS-Release).

## Structure du projet

```
arrera-branding/
├── src/
│   ├── pixmaps/
│   │   ├── arrera-logo.png
│   │   ├── arrera-logo.svg
│   │   ├── logo.png
│   │   └── baniere_*.png (black, blue, green, orange, etc.)
│   ├── fastfetch/
│   │   ├── config.jsonc
│   │   └── arrera-logo.txt
│   ├── plymouth/
│   │   ├── arrera.plymouth
│   │   ├── arrera.script
│   │   ├── logo.png
│   │   ├── progress_bar.png
│   │   └── progress_bg.png
│   ├── gdm/
│   │   ├── 99-arrera-login
│   │   ├── 99_arrera-branding.gschema.override
│   │   └── profile-gdm
│   ├── release/
│   │   ├── os-release
│   │   └── arrera-release
│   ├── scripts/
│   │   ├── 99-arrera-title.install
│   │   └── arrera-branding-guard.sh
│   └── systemd/
│       └── arrera-branding-guard.service
├── arrera-branding.spec
├── build.sh
├── LICENSE
└── README.md
```

## Construction du paquet RPM

Pour compiler le paquet RPM et SRPM :

```bash
./build.sh
```

Les paquets `.rpm` générés seront placés dans le dossier `output/`.
