Name:           arrera-branding
Version:        1.0.0
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

# 1. Pixmaps
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -a src/pixmaps/* %{buildroot}%{_datadir}/pixmaps/

for name in arrera-logo-text arrera-logo-text-dark system-logo-icon fedora-logo-icon fedora-logo fedora_logo fedora-logo-text fedora-logo-text-dark anaconda_header; do
    cp src/pixmaps/arrera-logo.png %{buildroot}%{_datadir}/pixmaps/${name}.png
    cp src/pixmaps/arrera-logo.svg %{buildroot}%{_datadir}/pixmaps/${name}.svg
done

# 2. Icônes hicolor
for size in 16x16 22x22 24x24 32x32 48x48 64x64 96x96 128x128 256x256 512x512; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}/apps
    for name in arrera-logo arrera-logo-text arrera-logo-text-dark system-logo-icon fedora-logo-icon fedora-logo fedora-logo-text fedora-logo-text-dark; do
        cp src/pixmaps/arrera-logo.png %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/${name}.png
    done
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
for name in arrera-logo arrera-logo-text arrera-logo-text-dark system-logo-icon fedora-logo-icon fedora-logo fedora-logo-text fedora-logo-text-dark; do
    cp src/pixmaps/arrera-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/${name}.svg
done

# 3. Anaconda
mkdir -p %{buildroot}%{_datadir}/anaconda/pixmaps
cp src/pixmaps/arrera-logo.png %{buildroot}%{_datadir}/anaconda/pixmaps/sidebar-logo.png
cp src/pixmaps/arrera-logo.png %{buildroot}%{_datadir}/anaconda/pixmaps/anaconda_header.png
cp src/pixmaps/arrera-logo.png %{buildroot}%{_datadir}/anaconda/pixmaps/topbar-bg.png

# 4. Fastfetch
mkdir -p %{buildroot}%{_sysconfdir}/fastfetch
cp src/fastfetch/config.jsonc %{buildroot}%{_sysconfdir}/fastfetch/config.jsonc
cp src/fastfetch/arrera-logo.txt %{buildroot}%{_sysconfdir}/fastfetch/arrera-logo.txt

# 5. Thème Plymouth
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/arrera
cp src/plymouth/* %{buildroot}%{_datadir}/plymouth/themes/arrera/

# 6. Configuration de l'écran de connexion GDM
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/gdm.d
cp src/gdm/99-arrera-login %{buildroot}%{_sysconfdir}/dconf/db/gdm.d/99-arrera-login

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
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
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/plymouth/themes/arrera/*
%config(noreplace) %{_sysconfdir}/fastfetch/*
%config(noreplace) %{_sysconfdir}/dconf/db/gdm.d/99-arrera-login

%changelog
* Tue Aug 25 2026 Arrera Software <contact@arrera.org> - 1.0.0-1
- Initial release of Arrera Branding package
