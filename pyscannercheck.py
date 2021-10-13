#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pyscannercheck.py - Un modeste outil pour identifier les problèmes
# de scanner sous Manjaro afin des les résoudre rapidement et surement
# Copyright (c) 2020 Olivier Girard <olivier@openshot.org>
#
# pyscannercheck is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pyscannercheck is distributed in the hope that it will be useful,
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
date_creation = "06-12-2020"

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
f = open("pyscannercheck.log", "w")


def append_output_check(output, title):
    divider = "--------------------------------------------------------------------------------------------------------"
    output = "%s\n%s\n%s\n%s\n\n" % (divider, title, divider, output)
    print(output)
    f.write(output)


# Header of the file - pour le fun lol
header_text = "pyscannercheck log file for scanner issues and more %s - %s" % (version, datetime.now())
append_output_check("Ce fichier contient un certain nombre de commandes qui permettront, à la fois de "
                    "fournir suffisament d'information sur la configuration et sur le scanner, afin "
                    "de pouvoir aider manuellement l'utilisateur à faire fonctionner son scanner et "
                    "plus encore", header_text)


# Cherche la version de Manjaro et plus (desktop, reseaux...)=> cat /etc/lsb-release
cmd = 'cat /etc/lsb-release'
process = subprocess.getoutput(cmd)
append_output_check(process, "Info Distribution Version")

# Info sur les port usb => lsusb : idealement lsusb -d vendorId -vvv
process = subprocess.getoutput(["lsusb"])
append_output_check(str(process), "Info Periphériques Usb")

# Info sur le materiel et reseau avec Inxi => inxi -Fldxxxz
cmd = 'inxi -Fldxxxz'
process = subprocess.getoutput(cmd)
append_output_check(process, "Info Etendues Configuration")

# Determine le port du scanner (chercher les occurances sane-port)
cmd = ['cat /etc/services | grep san']
process = subprocess.getoutput(cmd)
append_output_check(process, "Info sur l'utilisation des ports du scanner")

# Affiche le nom du scanner =>scanimage -L
process = subprocess.Popen(["scanimage", "-L"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Affiche le nom du scanner")
process.kill()

# Fait un scan de test => scanimage -T
process = subprocess.Popen(["scanimage", "-T"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
append_output_check(str(process.stdout.read()), "Test du scanner avec une image")
process.kill()

# Liste toutes les régles udev
cmd = 'ls /lib/udev/rules.d/'
process = subprocess.getoutput(cmd)
append_output_check(process, "Liste toutes les règles udev")

# Obtenir tous les détails de la liste (!!énorme) redirigée dans le fichier listereglesane.txt
cmd = ['cat /lib/udev/rules.d/49-sane.rules  >listereglessane.txt 2>&1']
process = subprocess.getoutput(cmd)
append_output_check(process, "Affiche tous les détails dans le fichier listereglescane.txt")

# Detection du scanner en root =>sudo sane-find-scanner (-v)



# Detection des ports usb du scanner mais en passant par sane et non lsusb =>sudo sane-find-scanner -q



# Affiche la liste du matériel =< sudo dmesg > malistematos.txt



# Message de fermeture du Fichier
append_output_check("Ce script a crée un fichier appelé 'pyscannercheck.log qui contient toutes les sorties des commandes \n"
                    "affichées au-dessus. Ouvrer ce fichier et poster le sur le forum. Toutes ces informations nous \n"
                    "aiderons à trouver le plus rapidement la solution à votre problème de scanner. D'autres commandes non incluses \n"
                    "dans ce fichier seront peut-être necessaire à votre cas.", "Fichier de Deboguage Scanner 'pyscannercheck.log'")

# Fermeture du fichier proprement dis
f.close()