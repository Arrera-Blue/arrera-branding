#!/bin/bash
# Arrera Branding Guard : Restaure automatiquement l'identité Arrera après toute mise à jour
MASTER_PRETTY=""
if [ -f /usr/share/arrera-branding/os-release ]; then
    MASTER_PRETTY=$(grep -E '^PRETTY_NAME=' /usr/share/arrera-branding/os-release | cut -d= -f2 | tr -d '"')
    if [ -n "$MASTER_PRETTY" ] && ! grep -q "PRETTY_NAME=\"${MASTER_PRETTY}\"" /usr/lib/os-release 2>/dev/null; then
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
    TITLE="Arrera Blue-dev 2026"
    [ -n "$MASTER_PRETTY" ] && TITLE="$MASTER_PRETTY"
    for conf in /boot/loader/entries/*.conf; do
        [ -f "$conf" ] || continue
        sed -i "s/^title Fedora Linux/title ${TITLE}/g" "$conf"
        sed -i "s/^title Fedora/title ${TITLE}/g" "$conf"
    done
fi
exit 0
