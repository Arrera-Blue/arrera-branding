%global edition education

# Configuration dynamique par édition
%if "%{edition}" == "education"
%global edition_name Éducation
%global edition_variant Education Edition
%global has_plymouth 1
%global has_background_logo 1
%elif "%{edition}" == "enterprise"
%global edition_name Entreprise
%global edition_variant Enterprise Edition
%global has_plymouth 1
%global has_background_logo 1
%elif "%{edition}" == "server"
%global edition_name Serveur
%global edition_variant Server Edition
%global has_plymouth 0
%global has_background_logo 0
%else
%global edition home
%global edition_name Home
%global edition_variant Home Edition
%global has_plymouth 1
%global has_background_logo 1
%endif

Name:           arrera-branding-%{edition}
Version:        2026.beta.1
Release:        6%{?dist}
Summary:        Visual assets and branding for Arrera Linux (%{edition_name} Edition)
License:        CC-BY-SA-4.0
URL:            https://github.com/Arrera-Blue/arrera-branding
Source0:        arrera-branding-%{version}.tar.gz
BuildArch:      noarch

%{!?_unitdir: %global _unitdir %{_prefix}/lib/systemd/system}

BuildRequires:  systemd-rpm-macros

Requires:       hicolor-icon-theme
Requires:       fastfetch
Requires:       dconf
Requires:       systemd
%if %{has_plymouth}
Requires:       plymouth-plugin-script
%endif

Provides:       arrera-branding = %{version}-%{release}
Provides:       arrera-branding-edition = %{version}-%{release}

# Conflits mutuels entre éditions
%if "%{edition}" == "home"
Conflicts:      arrera-branding-education arrera-branding-enterprise arrera-branding-server
%elif "%{edition}" == "education"
Conflicts:      arrera-branding-home arrera-branding-enterprise arrera-branding-server
%elif "%{edition}" == "enterprise"
Conflicts:      arrera-branding-home arrera-branding-education arrera-branding-server
%elif "%{edition}" == "server"
Conflicts:      arrera-branding-home arrera-branding-education arrera-branding-enterprise
%endif

%description
Visual assets, logos, and system branding for Arrera Linux %{edition_name} Edition across GNOME and GDM.
This autonomous RPM package includes all common Arrera branding assets and edition-specific identity configurations.

%prep
%autosetup -n arrera-branding-%{version}

%build
# Aucune compilation binaire requise (assets statiques)

%install
rm -rf %{buildroot}

# 1. Pixmaps Arrera
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -a common/pixmaps/* %{buildroot}%{_datadir}/pixmaps/

# 2. Icônes hicolor Arrera
for size in 16x16 22x22 24x24 32x32 48x48 64x64 96x96 128x128 256x256 512x512; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}/apps
    cp common/pixmaps/arrera-logo.png %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/arrera-logo.png
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp common/pixmaps/arrera-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/arrera-logo.svg

# 3. Fastfetch
mkdir -p %{buildroot}%{_sysconfdir}/fastfetch
cp common/fastfetch/config.jsonc %{buildroot}%{_sysconfdir}/fastfetch/config.jsonc
cp common/fastfetch/arrera-logo.txt %{buildroot}%{_sysconfdir}/fastfetch/arrera-logo.txt

# 4. Thème Plymouth Arrera (inclus uniquement pour Home, Éducation et Entreprise)
%if %{has_plymouth}
mkdir -p %{buildroot}%{_datadir}/plymouth/themes/arrera
cp common/plymouth/* %{buildroot}%{_datadir}/plymouth/themes/arrera/
%endif

# 5. Configuration de l'écran de connexion GDM & GSettings
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
cp common/gdm/99_arrera-branding.gschema.override %{buildroot}%{_datadir}/glib-2.0/schemas/99_arrera-branding.gschema.override
mkdir -p %{buildroot}%{_sysconfdir}/dconf/profile
cp common/gdm/profile-gdm %{buildroot}%{_sysconfdir}/dconf/profile/gdm
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/gdm.d
cp common/gdm/99-arrera-login %{buildroot}%{_sysconfdir}/dconf/db/gdm.d/99-arrera-login

# 6. Hook de titre GRUB / Kernel (/etc/kernel/install.d/)
mkdir -p %{buildroot}%{_sysconfdir}/kernel/install.d
install -m 755 common/scripts/99-arrera-title.install %{buildroot}%{_sysconfdir}/kernel/install.d/99-arrera-title.install

# 7. Scripts système Arrera (/usr/libexec/)
mkdir -p %{buildroot}%{_libexecdir}
install -m 755 common/scripts/arrera-branding-guard.sh %{buildroot}%{_libexecdir}/arrera-branding-guard.sh

# 8. Services systemd Arrera
mkdir -p %{buildroot}%{_unitdir}
install -m 644 common/systemd/arrera-branding-guard.service %{buildroot}%{_unitdir}/arrera-branding-guard.service

# 9. Fichiers maîtres de l'identité système de cette édition (/usr/share/arrera-branding/)
mkdir -p %{buildroot}%{_datadir}/arrera-branding
cp editions/%{edition}/os-release %{buildroot}%{_datadir}/arrera-branding/
cp editions/%{edition}/arrera-release %{buildroot}%{_datadir}/arrera-branding/

# 10. Background Logo pour l'extension GNOME (Home, Éducation, Entreprise)
%if %{has_background_logo}
mkdir -p %{buildroot}%{_datadir}/backgrounds/arrera
if [ -d editions/%{edition}/background-logo ]; then
    cp -a editions/%{edition}/background-logo/* %{buildroot}%{_datadir}/backgrounds/arrera/ 2>/dev/null || :
    mkdir -p %{buildroot}%{_datadir}/pixmaps
    cp -a editions/%{edition}/background-logo/logo.png %{buildroot}%{_datadir}/pixmaps/background-logo.png 2>/dev/null || :
    cp -a editions/%{edition}/background-logo/logo-dark.png %{buildroot}%{_datadir}/pixmaps/background-logo-dark.png 2>/dev/null || :
fi
%endif

# 11. Logo GDM propre à cette édition
if [ -f editions/%{edition}/gdm-logo.png ]; then
    mkdir -p %{buildroot}%{_datadir}/pixmaps
    cp -f editions/%{edition}/gdm-logo.png %{buildroot}%{_datadir}/pixmaps/arrera-gdm-logo.png
fi

%post
# 0. Services systemd Arrera
if [ -x /usr/bin/systemctl ]; then
    /usr/bin/systemctl daemon-reload &>/dev/null || :
    /usr/bin/systemctl enable arrera-branding-guard.service &>/dev/null || :
fi

# 1. Remplacement des bannières Thème CLAIR (Logo Bleu) pour GNOME / Paramètres "À propos"
if [ -f %{_datadir}/pixmaps/baniere_blue.png ]; then
    for light_name in fedora-logo-text fedora-logo fedora_logo fedora_logo_med system-logo-icon fedora-logo-icon fedora-logo-small; do
        cp -f %{_datadir}/pixmaps/baniere_blue.png %{_datadir}/pixmaps/${light_name}.png 2>/dev/null || :
    done
fi

# 2. Remplacement des bannières Thème SOMBRE (Logo Blanc) pour GDM et GNOME Dark
if [ -f %{_datadir}/pixmaps/baniere_white.png ]; then
    for dark_name in arrera-logo-text-dark fedora-logo-text-dark system-logo-white fedora_whitelogo_med; do
        cp -f %{_datadir}/pixmaps/baniere_white.png %{_datadir}/pixmaps/${dark_name}.png 2>/dev/null || :
    done
fi

# 3. Logo GDM propre à cette édition (remplace fedora-gdm-logo et garantit arrera-gdm-logo)
if [ -f %{_datadir}/pixmaps/arrera-gdm-logo.png ]; then
    cp -f %{_datadir}/pixmaps/arrera-gdm-logo.png %{_datadir}/pixmaps/fedora-gdm-logo.png 2>/dev/null || :
fi

# 4. Remplacement des logos ronds/carrés dans pixmaps
if [ -f %{_datadir}/pixmaps/arrera-logo.png ]; then
    cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/pixmaps/system-logo-icon.png 2>/dev/null || :
    cp -f %{_datadir}/pixmaps/arrera-logo.png %{_datadir}/pixmaps/fedora-logo-icon.png 2>/dev/null || :
fi
if [ -f %{_datadir}/pixmaps/arrera-logo.svg ]; then
    cp -f %{_datadir}/pixmaps/arrera-logo.svg %{_datadir}/pixmaps/fedora_whitelogo.svg 2>/dev/null || :
    cp -f %{_datadir}/pixmaps/arrera-logo.svg %{_datadir}/pixmaps/fedora-logo.svg 2>/dev/null || :
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

# 9. Initialisation de l'identité Arrera pour cette édition
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

# Configuration GRUB distributor
if [ -f /etc/default/grub ]; then
    sed -i 's/^GRUB_DISTRIBUTOR=.*/GRUB_DISTRIBUTOR="Arrera Blue 2026 (%{edition_name})"/' /etc/default/grub 2>/dev/null || :
fi

# Correction immédiate des entrées BLS existantes
if [ -d /boot/loader/entries ]; then
    for conf in /boot/loader/entries/*.conf; do
        [ -f "$conf" ] || continue
        sed -i 's/^title Fedora.*/title Arrera Blue-dev 2026 (%{edition_name})/g' "$conf" 2>/dev/null || :
    done
fi

# 10. Activation ou réinitialisation de Plymouth
%if %{has_plymouth}
if [ -x /usr/sbin/plymouth-set-default-theme ]; then
    /usr/sbin/plymouth-set-default-theme -R arrera &>/dev/null || :
fi
%else
if [ -x /usr/sbin/plymouth-set-default-theme ]; then
    /usr/sbin/plymouth-set-default-theme --reset 2>/dev/null || /usr/sbin/plymouth-set-default-theme -R details 2>/dev/null || :
fi
%endif

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
%{_datadir}/glib-2.0/schemas/99_arrera-branding.gschema.override
%config(noreplace) %{_sysconfdir}/fastfetch/*
%config(noreplace) %{_sysconfdir}/dconf/profile/gdm
%config(noreplace) %{_sysconfdir}/dconf/db/gdm.d/99-arrera-login
%{_sysconfdir}/kernel/install.d/99-arrera-title.install
%{_libexecdir}/arrera-branding-guard.sh
%{_unitdir}/arrera-branding-guard.service
%{_datadir}/arrera-branding/*
%if %{has_plymouth}
%{_datadir}/plymouth/themes/arrera/*
%endif
%if %{has_background_logo}
%{_datadir}/backgrounds/arrera/*
%endif

%changelog
* Thu Oct 01 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-6
- Build autonomous RPM packages per edition:
  * arrera-branding-home.rpm: Home edition with Plymouth
  * arrera-branding-education.rpm: Education edition with Plymouth
  * arrera-branding-enterprise.rpm: Enterprise edition with Plymouth
  * arrera-branding-server.rpm: Server edition without Plymouth (text boot)
- Share common visual assets (pixmaps, fastfetch, gdm, scripts, systemd) with zero duplication
- Make 99-arrera-title.install and arrera-branding-guard dynamically read PRETTY_NAME

* Thu Oct 01 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-5
- Remove obsolete Anaconda installer assets, profiles and icon overrides (Calamares is now used)
- Remove obsolete arrera-post-install-cleanup script and service (cleanup handled by Calamares / kickstart)

* Sat Sep 19 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-4
- Fix fastfetch logo indentation and adjust padding

* Sat Sep 19 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-3
- Add systemd-rpm-macros BuildRequires and fallback definition for _unitdir

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
