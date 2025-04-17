# nodo_luces
Programa en python, para la configuración de las luces.

Instalar dependencias 
pip3 install requeriments.txt

Instalar PyDMXControl
Sustutuir VERSION la version que tengas de python
Despues ir a la carpeta /usr/local/lib/python[VERSION]/dist-packages/PyDMXControl/web/_routes.py
Y en el archivo ir a routes = Blueprint(''), __name__, url_prefix='/')
Y modificarlo por
Y en el archivo ir a routes = Blueprint('dmx'), __name__, url_prefix='/')

Archivo para que el programa se ejecute, cuando se inicie la maquina
En lugar, poner el lugar donde estara la maquina
echo "[Unit]
Description=Iniciar luces

[Service]
ExecStart=/usr/bin/python3 /root/nodo_luces/luces_sockets.py lugar
Restart=always
StandardOutput=journal
StandardError=journal
SyslogIdentifier=programa

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/auto-restart.service

Programar el python para que se ejecute al inicio
systemctl daemon-reload
systemctl enable auto-restart.service
systemctl start auto-restart.service
systemctl status auto-restart.service
systemctl stop auto-restart.service
systemctl restart auto-restart.service
/usr/bin/python3 /nodo_luces/luces_sockets.py lugar

Comando para ver los logs
journalctl -u auto-restart.service

Comando para borrar los logs 
journalctl --vacuum-size=1M -u auto-restart.service

Comando para ver los registros en tiempo real
journalctl -fu auto-restart.service

Comando para borrar logs
journalctl --vacuum-size=100M --vacuum-time=1d -u auto-restart.service

echo "[Unit]
Description=Iniciar luces

[Service]
ExecStart=/usr/bin/python3 /nodo_luces/luces_sockets.py garage
Restart=always
StandardOutput=journal
StandardError=journal
SyslogIdentifier=luces_sockets

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/auto-restart.service