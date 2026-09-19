Name:           arrera-branding
Version:        2026.beta.1
Release:        2%{?dist}
Summary:        Visual assets and branding for Arrera Linux
License:        CC-BY-SA-4.0
URL:            https://github.com/Arrera-Blue/arrera-branding
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       hicolor-icon-theme
Requires:       fastfetch
Requires:       plymouth-plugin-script
Requires:       dconf
Requires:       systemd

%description
Visual assets, logos, and branding configurations for Arrera Linux.
Replaces default upstream branding across GNOME, Anaconda, and GDM.

%prep
%autosetup

%build
# Aucune compilation binaire requise (assets statiques)

%install
rm -rf %{buildroot}

# 1. Pixmaps Arrera
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -a src/pixmaps/* %{buildroot}%{_datadir}/pixmaps/

# 2. Icônes hicolor Arrera
for size in 16x16 22x22 24x24 32x32 48x48 64x64 96x96 128x128 256x256 512x512; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}/apps
    cp src/pixmaps/arrera-logo.png %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/arrera-logo.png
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp src/pixmaps/arrera-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/arrera-logo.svg

# 3. Fastfetch
mkdir -p %{buildroot}%{_sysconfdir}/fastfetch
cp src/fastfetch/config.jsonc %{buildroot}%{_sysconfdir}/fastfetch/config.jsonc
cp src/fastfetch/arrera-logo.txt %{buildroot}%{_sysconfdir}/fastfetch/arrera-logo.txt

# 4. Thème Plymouth
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/arrera
cp src/plymouth/* %{buildroot}%{_datadir}/plymouth/themes/arrera/

# 5. Configuration de l'écran de connexion GDM & GSettings
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
cp src/gdm/99_arrera-branding.gschema.override %{buildroot}%{_datadir}/glib-2.0/schemas/99_arrera-branding.gschema.override
mkdir -p %{buildroot}%{_sysconfdir}/dconf/profile
cp src/gdm/profile-gdm %{buildroot}%{_sysconfdir}/dconf/profile/gdm
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/gdm.d
cp src/gdm/99-arrera-login %{buildroot}%{_sysconfdir}/dconf/db/gdm.d/99-arrera-login

# 6. Assets Anaconda Arrera - stockés dans /usr/share/arrera/anaconda/ (évite conflit avec le paquet anaconda)
mkdir -p %{buildroot}%{_datadir}/arrera/anaconda/workstation
cp src/anaconda/workstation/* %{buildroot}%{_datadir}/arrera/anaconda/workstation/

# 7. Profils Anaconda Arrera (/etc/anaconda/profile.d/)
mkdir -p %{buildroot}%{_sysconfdir}/anaconda/profile.d
cp src/anaconda/profile.d/* %{buildroot}%{_sysconfdir}/anaconda/profile.d/

# 8. Hook de titre GRUB / Kernel (/etc/kernel/install.d/)
mkdir -p %{buildroot}%{_sysconfdir}/kernel/install.d
install -m 755 src/scripts/99-arrera-title.install %{buildroot}%{_sysconfdir}/kernel/install.d/99-arrera-title.install

# 9. Scripts système Arrera (/usr/libexec/)
mkdir -p %{buildroot}%{_libexecdir}
install -m 755 src/scripts/arrera-branding-guard.sh %{buildroot}%{_libexecdir}/arrera-branding-guard.sh
install -m 755 src/scripts/arrera-post-install-cleanup.sh %{buildroot}%{_libexecdir}/arrera-post-install-cleanup.sh

# 10. Services systemd Arrera
mkdir -p %{buildroot}%{_unitdir}
install -m 644 src/systemd/arrera-branding-guard.service %{buildroot}%{_unitdir}/arrera-branding-guard.service
install -m 644 src/systemd/arrera-post-install-cleanup.service %{buildroot}%{_unitdir}/arrera-post-install-cleanup.service

# 11. Sauvegardes de référence de l'identité système (/usr/share/arrera-branding/)
mkdir -p %{buildroot}%{_datadir}/arrera-branding
cp src/release/* %{buildroot}%{_datadir}/arrera-branding/

%post
# 0. Services systemd Arrera
if [ -x /usr/bin/systemctl ]; then
    /usr/bin/systemctl daemon-reload &>/dev/null || :
    /usr/bin/systemctl enable arrera-branding-guard.service &>/dev/null || :
    /usr/bin/systemctl enable arrera-post-install-cleanup.service &>/dev/null || :
fi

# 1. Remplacement des bannières Thème CLAIR (Logo Bleu) pour GNOME / Paramètres "À propos"
if [ -f %{_datadir}/pixmaps/baniere_blue.png ]; then
    for light_name in fedora-logo-text fedora-logo fedora_logo fedora_logo_med system-logo-icon fedora-logo-icon fedora-logo-small anaconda_header; do
        cp -f %{_datadir}/pixmaps/baniere_blue.png %{_datadir}/pixmaps/${light_name}.png 2>/dev/null || :
    done
fi

# 2. Remplacement des bannières Thème SOMBRE (Logo Blanc) pour GDM et GNOME Dark
if [ -f %{_datadir}/pixmaps/baniere_white.png ]; then
    for dark_name in arrera-logo-text-dark fedora-logo-text-dark system-logo-white fedora_whitelogo_med fedora-gdm-logo; do
        cp -f %{_datadir}/pixmaps/baniere_white.png %{_datadir}/pixmaps/${dark_name}.png 2>/dev/null || :
    done
fi

# 3. Remplacement des logos ronds/carrés dans pixmaps
if [ -f %{_datadir}/pixmaps/arrera-logo.png ]; then
    cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/pixmaps/system-logo-icon.png 2>/dev/null || :
    cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/pixmaps/fedora-logo-icon.png 2>/dev/null || :
fi
if [ -f %{_datadir}/pixmaps/arrera-logo.svg ]; then
    cp -f %{_datadir}/pixmaps/arrera-logo.svg %{_datadir}/pixmaps/fedora_whitelogo.svg 2>/dev/null || :
    cp -f %{_datadir}/pixmaps/arrera-logo.svg %{_datadir}/pixmaps/fedora-logo.svg 2>/dev/null || :
fi

# 4. Branding Anaconda Arrera - copie depuis /usr/share/arrera/anaconda/ (pas de conflit RPM)
if [ -d %{_datadir}/arrera/anaconda/workstation ] && [ -d %{_datadir}/anaconda/pixmaps/workstation ]; then
    cp -f %{_datadir}/arrera/anaconda/workstation/sidebar-logo.png %{_datadir}/anaconda/pixmaps/workstation/sidebar-logo.png 2>/dev/null || :
    cp -f %{_datadir}/arrera/anaconda/workstation/sidebar-logo_flavor.png %{_datadir}/anaconda/pixmaps/workstation/sidebar-logo_flavor.png 2>/dev/null || :
    cp -f %{_datadir}/arrera/anaconda/workstation/sidebar-bg.png %{_datadir}/anaconda/pixmaps/workstation/sidebar-bg.png 2>/dev/null || :
    cp -f %{_datadir}/arrera/anaconda/workstation/topbar-bg.png %{_datadir}/anaconda/pixmaps/workstation/topbar-bg.png 2>/dev/null || :
    # Remplacer le CSS Fedora par le CSS Arrera
    cp -f %{_datadir}/arrera/anaconda/workstation/arrera-workstation.css %{_datadir}/anaconda/pixmaps/workstation/fedora-workstation.css 2>/dev/null || :
fi
# Bannière header pour l'installateur
if [ -f %{_datadir}/pixmaps/baniere_blue.png ] && [ -d %{_datadir}/anaconda/pixmaps ]; then
    cp -f %{_datadir}/pixmaps/baniere_blue.png %{_datadir}/anaconda/pixmaps/anaconda_header.png 2>/dev/null || :
fi

# 4bis. Remplacement des icônes d'application Anaconda / Installateur (menu, dock, bureau)
if [ -f %{_datadir}/pixmaps/anaconda.png ]; then
    mkdir -p %{_datadir}/icons/hicolor/256x256/apps
    cp -f %{_datadir}/pixmaps/anaconda.png %{_datadir}/icons/hicolor/256x256/apps/anaconda.png 2>/dev/null || :
    find %{_datadir}/icons -type f \( -iname "*anaconda*.png" -o -iname "*AnacondaInstaller*.png" \) -exec cp -f %{_datadir}/pixmaps/anaconda.png {} \; 2>/dev/null || :
fi
if [ -f %{_datadir}/pixmaps/anaconda.svg ]; then
    find %{_datadir}/icons -type f \( -iname "*anaconda*.svg" -o -iname "*AnacondaInstaller*.svg" \) -exec cp -f %{_datadir}/pixmaps/anaconda.svg {} \; 2>/dev/null || :
fi

# 5. Remplacement des icônes SVG/PNG dans tous les thèmes
if [ -f %{_datadir}/pixmaps/arrera-logo.svg ]; then
    find %{_datadir}/icons -type f \( -iname "*fedora*logo*.svg" -o -iname "*fedora*text*.svg" \) -exec cp -f %{_datadir}/pixmaps/arrera-logo.svg {} \; 2>/dev/null || :
fi
if [ -f %{_datadir}/pixmaps/arrera-logo.png ]; then
    find %{_datadir}/icons -type f \( -iname "*fedora*logo*.png" -o -iname "*fedora*text*.png" \) -exec cp -f %{_datadir}/pixmaps/arrera-logo.png {} \; 2>/dev/null || :
fi

# 6. Rafraîchissement des caches d'icônes
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    for theme_dir in %{_datadir}/icons/*; do
        if [ -d "$theme_dir" ]; then
            /usr/bin/gtk-update-icon-cache -f -t "$theme_dir" &>/dev/null || :
        fi
    done
fi

# 7. Compilation des schémas GSettings (GDM / GNOME)
if [ -x /usr/bin/glib-compile-schemas ]; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi

# 8. Mise à jour de la configuration dconf (GDM)
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
    chmod 644 %{_sysconfdir}/dconf/db/gdm 2>/dev/null || :
fi

# 9. Activation automatique du thème Plymouth Arrera
if [ -x /usr/sbin/plymouth-set-default-theme ]; then
    /usr/sbin/plymouth-set-default-theme -R arrera &>/dev/null || :
fi

# 10. Initialiser l'identité Arrera et les liens de compatibilité
if [ -f %{_datadir}/arrera-branding/os-release ]; then
    cp -f %{_datadir}/arrera-branding/os-release /usr/lib/os-release 2>/dev/null || :
    cp -f %{_datadir}/arrera-branding/os-release /etc/os-release 2>/dev/null || :
fi
if [ -f %{_datadir}/arrera-branding/arrera-release ]; then
    cp -f %{_datadir}/arrera-branding/arrera-release /etc/arrera-release 2>/dev/null || :
    for release_file in fedora-release system-release redhat-release; do
        rm -f "/etc/$release_file" 2>/dev/null || :
        ln -sf /etc/arrera-release "/etc/$release_file" 2>/dev/null || :
    done
fi

# Configuration GRUB distributor si présent
if [ -f /etc/default/grub ]; then
    sed -i 's/^GRUB_DISTRIBUTOR=.*/GRUB_DISTRIBUTOR="Arrera Blue-dev 2026"/' /etc/default/grub 2>/dev/null || :
fi

# Corriger immédiatement les entrées BLS existantes
if [ -d /boot/loader/entries ]; then
    for conf in /boot/loader/entries/*.conf; do
        [ -f "$conf" ] || continue
        sed -i 's/^title Fedora Linux/title Arrera Blue-dev 2026/g' "$conf" 2>/dev/null || :
        sed -i 's/^title Fedora/title Arrera Blue-dev 2026/g' "$conf" 2>/dev/null || :
    done
fi

%postun
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
if [ -x /usr/bin/glib-compile-schemas ]; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
fi
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

%files
%license LICENSE
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/arrera-logo.png
%{_datadir}/icons/hicolor/scalable/apps/arrera-logo.svg
%{_datadir}/plymouth/themes/arrera/*
%{_datadir}/glib-2.0/schemas/99_arrera-branding.gschema.override
%config(noreplace) %{_sysconfdir}/fastfetch/*
%config(noreplace) %{_sysconfdir}/dconf/profile/gdm
%config(noreplace) %{_sysconfdir}/dconf/db/gdm.d/99-arrera-login
%{_datadir}/arrera/anaconda/workstation/*
%config(noreplace) %{_sysconfdir}/anaconda/profile.d/*
%{_sysconfdir}/kernel/install.d/99-arrera-title.install
%{_libexecdir}/arrera-branding-guard.sh
%{_libexecdir}/arrera-post-install-cleanup.sh
%{_unitdir}/arrera-branding-guard.service
%{_unitdir}/arrera-post-install-cleanup.service
%{_datadir}/arrera-branding/*

%changelog
* Sat Sep 19 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-2
- Add Anaconda installer profiles (arrera.conf and arrera-workstation.conf)
- Add kernel-install BLS title hook (99-arrera-title.install)
- Add arrera-branding-guard systemd service and script
- Add arrera-post-install-cleanup systemd service and script
- Add master release files in /usr/share/arrera-branding/

* Sat Sep 12 2026 Arrera Software <contact@arrera.org> - 1.1.7-1
- Add Arrera Anaconda installer application icon (anaconda.png and anaconda.svg)
- Overwrite default anaconda / AnacondaInstaller desktop icons in hicolor and system themes
- Fix Anaconda sidebar and branding assets

* Sat Sep 12 2026 Arrera Software <contact@arrera.org> - 1.1.6-1
- Update version to 1.1.6

* Sat Sep 12 2026 Arrera Software <contact@arrera.org> - 1.1.5-1
- Add sidebar-logo_flavor.png (Arrera Blue banner) displayed at top of Anaconda sidebar
- Update Anaconda CSS to use product-logo with correct positioning
- Fix sidebar-logo (small A icon) positioned at bottom of sidebar

* Sun Sep 06 2026 Arrera Software <contact@arrera.org> - 1.1.4-1
- Add Arrera Blue branding for Anaconda installer (sidebar logo, background, CSS)
- Replace fedora-workstation.css with Arrera blue theme in Anaconda
- Fix: store Anaconda assets in /usr/share/arrera/anaconda/ to avoid RPM file conflict with anaconda package

* Tue Sep 01 2026 Arrera Software <contact@arrera.org> - 1.1.3-1
- Set blue banner for light mode (GNOME About settings) and white banner for dark mode
- Enforce Arrera Blue-dev 2026 identity in os-release
