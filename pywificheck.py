#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pywificheck.py - Un modeste outil pour identifier les problèmes
# de wifi sous Manjaro afin des les résoudre rapidement et surement
# Copyright (c) 2020 Olivier Girard <olivier@openshot.org>
#
# pywificheck is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pywificheck is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# version initiale 0.01
# version 0.02 finalisation des commandes utilisateur normal
# version 0.03 proposée par fbe utilisation fichier json  très interressante non retenue + complexe utilisateur lambda
# version 0.04 ajout des commandes roots
# version 0.05 meilleur utilisation de subprocess

import sys
import os
import subprocess
from datetime import datetime

# version du script
version = "0.0.4"

# Date création initiale du script
date_creation = "01-12-2020"

# if __name__ == '__main__':
#
#     # Must be root to run some commands
#     current_user = subprocess.getoutput("whoami")
#     if current_user == 'root':
#         sys.exit(0)
#     else:
#         print("You must be root")
#         sys.exit(1)

# création du fichier de sortie
f = open("pycheckwifi.log", "w")


def append_output_check(output, title):
    divider = "------------------------------------------------------------------------------------------------------- "
    output = "%s\n%s\n%s\n%s\n\n" % (divider, title, divider, output)
    print(output)
    f.write(output)


# Header of the file - pour le fun lol
header_text = "pywificheck log file for wifi issues and more %s - %s" % (version, datetime.now())
append_output_check("Ce fichier contient un certain nombre de commandes qui permettront, à la fois de "
                    "fournir suffisament d'information sur la configuration et sur le réseau wifi, afin "
                    "de pouvoir aider manuellement l'utilisateur à faire fonctionner son wifi et "
                    "plus encore", header_text)

# Cherche la version de Manjaro et plus (desktop, reseaux...)=> cat /etc/lsb-release
cmd = 'cat /etc/lsb-release'
process = subprocess.getoutput(cmd)
append_output_check(process, "Info Distribution Version")

# Cherche les versions installées ou non de NetworkManager, iwd, wpa_supplicant=>Necessaire ? A voir selon retour


# Connaitre la zone Fr pour le wifi => iw reg get - note pour choisir FR sudo iw reg set FR non inclus
process = subprocess.run(["iw", "reg", "get"], capture_output=True, text=True).stdout
append_output_check(process, "Zone Wifi")

# Info sur les port usb => lsusb
process = subprocess.run(["lsusb"], capture_output=True, text=True).stdout
append_output_check(process, "Info Periphériques Usb")

# Info sur les port pci => lspci
process = subprocess.run(["lspci"], capture_output=True, text=True).stdout
append_output_check(process, "Info Périphériques Pci")

# Info sur le reseau avec Inxi => inxi -Nx
cmd = ['inxi', '-Nx']
process = subprocess.run(cmd, capture_output=True, text=True).stdout
append_output_check(process, "Info Inxi Réseau")

# Info sur le materiel et reseau avec Inxi => inxi -Fldxxxz
process = subprocess.run(["inxi", "-Fldxxxz"], capture_output=True, text=True).stdout
append_output_check(process, "Info Inxi Etendues Configuration")

# info iwconfig => iwconfig
with subprocess.Popen(["iwconfig"], universal_newlines=True, stdout=subprocess.PIPE) as process:
    append_output_check(process.stdout.read(), "Info Réseau")

# Info ifconfig => ifconfig
with subprocess.Popen(["ifconfig"], universal_newlines=True, stdout=subprocess.PIPE) as process:
    append_output_check(process.stdout.read(), "Info Réseau Standard")

# Info sur la connection en pci ? => lspci | grep -i net (et usb ?)
# cmd = ("lspci", "|", "grep", "-i", "net")
# process = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmd = ["lspci | grep -i net"]
process = subprocess.getoutput(cmd)
append_output_check(str(process), "Info Reseau Carte Pci")

# Info plus evoluees et differente du precedant => lspci -k -nn | grep -A 3 -i net
cmd = ["lspci -k -nn | grep -A 3 -i net"]
proc = subprocess.getoutput(cmd)
append_output_check(str(proc), "Info Réseau Etendue Carte Pci")

# Info sur les reseaux dispo (force et disponiblité) => nmcli dev wifi
process = subprocess.Popen(["nmcli", "dev", "wifi"], universal_newlines=True, stdout=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Info sur Wifi - Force et Disponibilité")
process.kill()

# Info sur les connections reseaux => nmcli connection show
process = subprocess.Popen(["nmcli", "connection", "show"], universal_newlines=True, stdout=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Info Connection SSID")

# Info liste peripheriques supportant wifi, ssid, mac add => iw dev
process = subprocess.Popen(["iw", "dev"], universal_newlines=True, stdout=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Info wifi-ssid-mac add")

# Indique si le bluetooth fonctionne => systemctl status bluetooth
process = subprocess.Popen(["systemctl", "status", "bluetooth"], universal_newlines=True, stdout=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Fonctionnement Bluetooth")

# Affiche les journaux pour NetworkManager => journalctl -u NetworkManager | tail -10
cmd = ["journalctl -u NetworkManager | tail -10"]
process = subprocess.getoutput(cmd)
append_output_check(process, "Affichage des journaux pour NetworkManager")

# Verification carte wifi/bt n'est pas desactivé => sudo rfkill list ===si soft blocked=yes =>pbme wifi logiciel
# si hard blocked=yes =< pbme wifi materiel resolvable avec sudo rfkill unblock all- Si rien pas de driver
# command = ["sudo rfkill list | grep \"root\""]
# process = subprocess.Popen(['sudo', 'rfkill', 'list', '|', 'grep', "\"root\""], universal_newlines=True, stdout=subprocess.PIPE)
process = subprocess.run(['sudo', 'rfkill', 'list'], capture_output=True, text=True).stdout
# process = subprocess.getoutput(command)
append_output_check(process, "Definition de l'activation ou pas de la carte")

# liste les reseaux disponibles en root => sudo iwlist scan
process = subprocess.run(['sudo', 'iwlist', 'scan'], capture_output=True, text=True).stdout
append_output_check(process, "Liste des réseaux disponibles")

# liste les reseaux visibles pour monreseau en root => sudo iw dev monreseau scan
# definition de la variable monreseau necessaire pour avoir la liste des reseaux disponibles
monreseau = ""
# Si mon reseau exist
if monreseau is not None:
    newprocess = subprocess.run(['sudo', 'iw', 'dev', 'monreseau', 'scan'], capture_output=True, text=True).stdout
    append_output_check(newprocess, "Listes des reseaux disponible pour mon lan perso")

# liste l'etat de la connection wifi en root => sudo iw dev monreseau link
monreseau = ""
if monreseau is not None:
    anotherprocess = subprocess.run(['sudo', 'iw', 'dev', 'monreseau', 'link'], capture_output=True, text=True).stdout
    append_output_check(anotherprocess, "Liste l'état de la connection wifi")

# Message de fermeture du Fichier
append_output_check(
    "Ce script a crée un fichier appelé 'pywificheck.log qui contient toutes les sorties des commandes \n"
    "affichées au-dessus. Ouvrer ce fichier et poster le sur le forum. Toutes ces informations nous \n"
    "aiderons à trouver le plus rapidement la solution à votre problème de wifi/réseau. D'autres commandes non incluses \n"
    "dans ce fichier seront peut-être necessaire à votre cas.", "Fichier de Deboguage Wifi 'pywificheck.log'")

# Fermeture du fichier proprement dis
f.close()
