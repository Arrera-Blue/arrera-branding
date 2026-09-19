#!/bin/bash
# Arrera Branding Guard : Restaure automatiquement l'identité Arrera après toute mise à jour
if [ -f /usr/share/arrera-branding/os-release ]; then
    if ! grep -q 'PRETTY_NAME="Arrera Blue-dev 2026"' /usr/lib/os-release 2>/dev/null; then
        cp -f /usr/share/arrera-branding/os-release /usr/lib/os-release
        cp -f /usr/share/arrera-branding/os-release /etc/os-release
    fi
fi
if [ -f /usr/share/arrera-branding/arrera-release ]; then
    cp -f /usr/share/arrera-branding/arrera-release /etc/arrera-release
    for f in fedora-release system-release redhat-release; do
        ln -sf /etc/arrera-release "/etc/$f" 2>/dev/null || true
    done
fi
if [ -d /boot/loader/entries ]; then
    for conf in /boot/loader/entries/*.conf; do
        [ -f "$conf" ] || continue
        sed -i 's/^title Fedora Linux/title Arrera Blue-dev 2026/g' "$conf"
        sed -i 's/^title Fedora/title Arrera Blue-dev 2026/g' "$conf"
    done
fi
exit 0
