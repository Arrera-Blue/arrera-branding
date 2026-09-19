#!/bin/bash
# 1. Désactiver l'auto-login GDM (retour au login utilisateur avec mot de passe)
if [ -f /etc/gdm/custom.conf ]; then
    sed -i '/AutomaticLoginEnable=True/d' /etc/gdm/custom.conf
    sed -i '/AutomaticLogin=arrera/d' /etc/gdm/custom.conf
    sed -i 's/AutomaticLoginEnable=True/AutomaticLoginEnable=False/g' /etc/gdm/custom.conf
fi

# 2. Supprimer le compte live "arrera" et conserver le compte créé lors de l'installation
if id "arrera" &>/dev/null; then
    OTHER_USER=$(awk -F: '$3 >= 1000 && $1 != "arrera" && $1 != "nobody" {print $1}' /etc/passwd | head -n 1)
    if [ -n "$OTHER_USER" ]; then
        pkill -9 -u arrera 2>/dev/null || true
        userdel -r -f arrera 2>/dev/null || true
        rm -rf /home/arrera
        rm -f /etc/sudoers.d/arrera
    fi
fi

# 3. Supprimer les raccourcis et autostarts de l'installateur
rm -f /home/arrera/Bureau/install-arrera.desktop
rm -f /home/arrera/Desktop/install-arrera.desktop
rm -f /home/arrera/.config/autostart/install-arrera.desktop
rm -f /home/arrera/.config/autostart/liveinst.desktop
rm -f /etc/xdg/autostart/install-arrera.desktop
rm -f /etc/xdg/autostart/liveinst.desktop
rm -f /usr/share/applications/install-arrera.desktop
rm -f /usr/share/applications/liveinst.desktop
rm -f /usr/share/applications/*anaconda*.desktop

# 4. Supprimer les règles Polkit du Live
rm -f /etc/polkit-1/rules.d/49-liveuser.rules
rm -f /etc/polkit-1/rules.d/50-anaconda.rules

# 5. Supprimer Anaconda du système installé
rpm -e --nodeps anaconda anaconda-live anaconda-install-env-deps anaconda-gui anaconda-tui liveinst 2>/dev/null || true

# 6. Auto-suppression de ce service
systemctl disable arrera-post-install-cleanup.service 2>/dev/null || true
rm -f /etc/systemd/system/arrera-post-install-cleanup.service
rm -f /usr/libexec/arrera-post-install-cleanup.sh
systemctl daemon-reload 2>/dev/null || true

exit 0
