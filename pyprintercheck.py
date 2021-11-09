#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pyprintercheck.py - Un modeste outil pour identifier les problèmes
# de scanner sous Manjaro afin des les résoudre rapidement et surement
# Copyright (c) 2020-2021 Olivier Girard <olivier@openshot.org>
#
# pyprintercheck is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pyprintercheck is distributed in the hope that it will be useful,
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

# Date création script
date_creation = "09-12-2020"

# if __name__ == '__main__':
#
#     # Must be root to run some commands
#     current_user = subprocess.getoutput("whoami")
#     if current_user == "root":
#         sys.exit(0)
#     else:
#         print("you must be root")
#         sys.exit(1)

# création du fichier de sortie
f = open("pyprintercheck.log","w")


def append_output_check(output, title):
    divider = "--------------------------------------------------------------------------------------------------------------------"
    output = "%s\n%s\n%s\n%s\n\n" % (divider, title, divider, output)
    print(output)
    f.write(output)


# Header of the file - pour le fun lol
header_text = "pyprintercheck log file for printer issues and more %s - %s" % (version, datetime.now())
append_output_check("Ce fichier contient un certain nombre de commandes qui permettront, à la fois de "
                    "fournir suffisament d'information sur la configuration et sur l'imprimante, afin "
                    "de pouvoir aider manuellement l'utilisateur à faire fonctionner son imprimante et "
                    "plus encore", header_text)


# Cherche la version de Manjaro et plus (desktop, reseaux...)=> cat /etc/lsb-release
cmd = 'cat /etc/lsb-release'
process = subprocess.getoutput(cmd)
append_output_check(process, "Info Distribution Version")

# Info sur les port usb => lsusb
process = subprocess.getoutput(["lsusb"])
append_output_check(str(process), "Info Periphériques Usb")

# Verification du chargement du module usb => lsmod | grep usblp
cmd = ["lsmod | grep usblp"]
# process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess, universal_newlines=True)
# output, error = cmd.communicate()
# if error:
#     append_output_check("%s" % error)
process = subprocess.getoutput(cmd)
append_output_check(process, "Verification du Chargement du module usb")

# Verification du chargement de l'imprimante par le systeme => systemctl status cups
process = subprocess.Popen(['systemctl', 'status', 'cups'], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Fonctionnement CUPS")
process.kill()

# verification du chargement des regles udev par le systeme =q systemctl status systemd-udevd-service
process = subprocess.Popen(['systemctl', 'status', 'systemd-udevd'], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Fonctionnement Regles UDEV")
process.kill()

# Info sur le materiel et reseau avec Inxi => inxi -Fldxxxz
cmd = 'inxi -Fldxxxz'
process = subprocess.getoutput(cmd)
append_output_check(process, "Info Etendues Configuration")

# Lister les journaux de cups => sudo cat /etc/cups/cups-files.conf
cmd = ['sudo cat /etc/cups/cups-files.conf']
process = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Fonctionnement CUPS")
process.kill()

#

# Message de fermeture du Fichier
append_output_check("Ce script a crée un fichier appelé 'pyprintercheck.log qui contient toutes les sorties des commandes \n"
                    "affichées au-dessus. Ouvrer ce fichier et poster le sur le forum. Toutes ces informations nous \n"
                    "aiderons à trouver le plus rapidement la solution à votre problème de bluetooth. D'autres commandes non incluses \n"
                    "dans ce fichier seront peut-être necessaire à votre cas.", "Fichier de Deboguage Imprimante 'pyprintercheck.log'")

# Fermeture du fichier proprement dis
f.close()

