Name:           arrera-branding
Version:        1.1.3
Release:        1%{?dist}
Summary:        Visual assets and branding for Arrera Linux
License:        CC-BY-SA-4.0
URL:            https://arrera.org/
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       hicolor-icon-theme
Requires:       fastfetch
Requires:       plymouth-plugin-script
Requires:       dconf

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

%post
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

# 4. Remplacement dynamique du branding Anaconda
mkdir -p %{_datadir}/anaconda/pixmaps 2>/dev/null || :
if [ -f %{_datadir}/pixmaps/baniere_blue.png ]; then
    cp -f %{_datadir}/pixmaps/baniere_blue.png %{_datadir}/anaconda/pixmaps/anaconda_header.png 2>/dev/null || :
    cp -f %{_datadir}/pixmaps/baniere_blue.png %{_datadir}/anaconda/pixmaps/sidebar-logo.png 2>/dev/null || :
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

# 10. Forcer l'identité Arrera Blue-dev 2026 dans os-release
if [ -f /usr/lib/os-release ]; then
    sed -i 's/^NAME=.*/NAME="Arrera"/' /usr/lib/os-release 2>/dev/null || :
    sed -i 's/^PRETTY_NAME=.*/PRETTY_NAME="Arrera Blue-dev 2026"/' /usr/lib/os-release 2>/dev/null || :
    sed -i 's/^VERSION=.*/VERSION="Blue-dev 2026"/' /usr/lib/os-release 2>/dev/null || :
    sed -i 's/^VERSION_ID=.*/VERSION_ID="2026"/' /usr/lib/os-release 2>/dev/null || :
    sed -i 's/^VERSION_CODENAME=.*/VERSION_CODENAME="Blue-dev"/' /usr/lib/os-release 2>/dev/null || :
    sed -i 's/^ID=.*/ID=arrera/' /usr/lib/os-release 2>/dev/null || :
    sed -i 's/^ID_LIKE=.*/ID_LIKE=fedora/' /usr/lib/os-release 2>/dev/null || :
    sed -i 's/^LOGO=.*/LOGO="fedora-logo-text"/' /usr/lib/os-release 2>/dev/null || :
    cp -f /usr/lib/os-release /etc/os-release 2>/dev/null || :
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

%changelog
* Tue Sep 01 2026 Arrera Software <contact@arrera.org> - 1.1.3-1
- Set blue banner for light mode (GNOME About settings) and white banner for dark mode
- Enforce Arrera Blue-dev 2026 identity in os-release
