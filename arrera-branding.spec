Name:           arrera-branding
Version:        1.0.1
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

# 5. Configuration de l'écran de connexion GDM
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/gdm.d
cp src/gdm/99-arrera-login %{buildroot}%{_sysconfdir}/dconf/db/gdm.d/99-arrera-login

%post
# 1. Remplacement dynamique du branding Fedora dans pixmaps
if [ -f %{_datadir}/pixmaps/arrera-logo.png ]; then
    for name in arrera-logo-text arrera-logo-text-dark system-logo-icon fedora-logo-icon fedora-logo fedora_logo fedora-logo-text fedora-logo-text-dark anaconda_header; do
        cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/pixmaps/${name}.png 2>/dev/null || :
        if [ -f %{_datadir}/pixmaps/arrera-logo.svg ]; then
            cp -f %{_datadir}/pixmaps/arrera-logo.svg %{_datadir}/pixmaps/${name}.svg 2>/dev/null || :
        fi
    done
fi

# 2. Remplacement dynamique du branding Anaconda
mkdir -p %{_datadir}/anaconda/pixmaps 2>/dev/null || :
if [ -f %{_datadir}/pixmaps/arrera-logo.png ]; then
    cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/anaconda/pixmaps/sidebar-logo.png 2>/dev/null || :
    cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/anaconda/pixmaps/anaconda_header.png 2>/dev/null || :
    cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/anaconda/pixmaps/topbar-bg.png 2>/dev/null || :
fi

# 3. Remplacement des icônes SVG/PNG dans tous les thèmes
if [ -f %{_datadir}/pixmaps/arrera-logo.svg ]; then
    find %{_datadir}/icons -type f \( -iname "*fedora*logo*.svg" -o -iname "*fedora*text*.svg" \) -exec cp -f %{_datadir}/pixmaps/arrera-logo.svg {} \; 2>/dev/null || :
fi
if [ -f %{_datadir}/pixmaps/arrera-logo.png ]; then
    find %{_datadir}/icons -type f \( -iname "*fedora*logo*.png" -o -iname "*fedora*text*.png" \) -exec cp -f %{_datadir}/pixmaps/arrera-logo.png {} \; 2>/dev/null || :
fi

# 4. Rafraîchissement des caches d'icônes
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    for theme_dir in %{_datadir}/icons/*; do
        if [ -d "$theme_dir" ]; then
            /usr/bin/gtk-update-icon-cache -f -t "$theme_dir" &>/dev/null || :
        fi
    done
fi

# 5. Mise à jour de la configuration dconf (GDM)
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

# 6. Activation automatique du thème Plymouth Arrera
if [ -x /usr/sbin/plymouth-set-default-theme ]; then
    /usr/sbin/plymouth-set-default-theme -R arrera &>/dev/null || :
fi

%postun
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
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
%config(noreplace) %{_sysconfdir}/fastfetch/*
%config(noreplace) %{_sysconfdir}/dconf/db/gdm.d/99-arrera-login

%changelog
* Thu Aug 27 2026 Arrera Software <contact@arrera.org> - 1.0.1-1
- Fix file conflicts with fedora-logos by dynamically overriding in post scriptlet
- Add automated Plymouth theme activation
- Add complete GDM and Fastfetch asset deployment
