#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pybluetoothcheck.py - Un modeste outil pour identifier les problèmes
# de scanner sous Manjaro afin des les résoudre rapidement et surement
# Copyright (c) 2020 Olivier Girard <olivier@openshot.org>
#
# pybluetoothcheck is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pybluetoothcheck is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import subprocess
from datetime import datetime

# version du script
version = "0.0.1"

# if __name__ == '__main__':
#
#     # must be root to run some commands
#     current_user = subprocess.getoutput("whoami")
#     if current_user == 'root':
#         sys.exit(0)
#     else:
#         print("you must bee root")
#         sys.exit(1)

# Date création script
date_creation = "06-12-2020"

# création du fichier de sortie
f = open("pybluetoothcheck.log", "w")


def append_output_check(output, title):
    divider = "--------------------------------------------------------------------------------------------------------------------"
    output = "%s\n%s\n%s\n%s\n\n" % (divider, title, divider, output)
    print(output)
    f.write(output)


# Header of the file - pour le fun lol
header_text = "pybluetoothcheck log file for bluetooth issues and more %s - %s" % (version, datetime.now())
append_output_check("Ce fichier contient un certain nombre de commandes qui permettront, à la fois de "
                    "fournir suffisament d'information sur la configuration et sur le bluetooth, afin "
                    "de pouvoir aider manuellement l'utilisateur à faire fonctionner son bluetooth et "
                    "plus encore", header_text)


# Cherche la version de Manjaro et plus (desktop, reseaux...)=> cat /etc/lsb-release
cmd = 'cat /etc/lsb-release'
process = subprocess.getoutput(cmd)
append_output_check(process, "Info Distribution Version")

# Info sur les port usb => lsusb
process = subprocess.getoutput(["lsusb"])
append_output_check(str(process), "Info Periphériques Usb")

# Info sur le materiel et reseau avec Inxi => inxi -Fldxxxz
cmd = 'inxi -Fldxxxz'
process = subprocess.getoutput(cmd)
append_output_check(process, "Info Etendues Configuration")

# Indique si le bluetooth fonctionne => systemctl status bluetooth
process = subprocess.Popen(["systemctl", "status", "bluetooth"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Fonctionnement Bluetooth")
process.kill()

# Verification carte wifi/bt n'est pas desactivé => sudo rfkill list ===si soft blocked=yes =>pbme wifi logiciel
# si hard blocked=yes =< pbme wifi materiel resolvable avec sudo rfkill unblock all



# Message de fermeture du Fichier
append_output_check("Ce script a crée un fichier appelé 'pybluetoothcheck.log qui contient toutes les sorties des commandes \n"
                    "affichées au-dessus. Ouvrer ce fichier et poster le sur le forum. Toutes ces informations nous \n"
                    "aiderons à trouver le plus rapidement la solution à votre problème de bluetooth. D'autres commandes non incluses \n"
                    "dans ce fichier seront peut-être necessaire à votre cas.", "Fichier de Deboguage Bluetooth 'pybluetooth.log'")

# Fermeture du fichier proprement dis
f.close()