#!/bin/bash

# Actualizar y mejorar los paquetes existentes
pkg update && pkg upgrade -y

# Instalar Python, pip y Git
pkg install python -y
pkg install python-pip -y
pkg install git -y

# Clonar el repositorio del bot
git clone https://github.com/Eliasar54/Bot-de-Telegram-ia.git

# Navegar al directorio del bot
cd Bot-de-Telegram-ia

# Instalar las dependencias necesarias
pip install telepot requests colorama

# Ejecutar el bot
python Bot.py
