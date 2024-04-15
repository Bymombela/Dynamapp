from netmiko import ConnectHandler

# Definir los detalles de conexión SSH
ip = input('Direccion ip a conectar: ')
username = input('diga el username para el ssh')
password = input('ingresa la contrasena del ssh')



device = {
    'device_type': 'cisco_ios',
    'ip': ip,  # Reemplaza con la dirección IP de tu dispositivo
    'username': username,  # Reemplaza con tu nombre de usuario SSH
    'password': 'cisco',  # Reemplaza con tu contraseña SSH
    'secret': 'cisco',
}

# Iniciar la conexión SSH
ssh_connection = ConnectHandler(**device)

# Ingresar al modo de configuración
ssh_connection.enable()


# También puedes cambiar el hostname



while True:
    salir = input('Presiona Q para salirse o otra letra para seguir').lower()
    if salir == 'q':
        break
    conf_m = input('Presiona E para Enable y C para modo configuracion').lower()
    if conf_m == 'c':
        ssh_connection.config_mode()
        command = input('Ingresa un comando: ')
        output = ssh_connection.send_config_set(command)
        print(output)
        continue

        
    command = input('Ingresa un comando: ')
    output = ssh_connection.send_command(command)
    print(output)

# Salir del modo de configuración
ssh_connection.exit_config_mode()
# Cerrar la conexión SSH
ssh_connection.disconnect()
    



from scapy.all import Ether, LLDP,srp
from collections import defaultdict

def descubrir_topologia():
    # Enviar un paquete LLDP para descubrir vecinos
    lldp_request = Ether(dst="01:80:c2:00:00:0e") / LLDP()
    lldp_response, _ = srp(lldp_request, iface="eth0", timeout=2, verbose=False)
    
    # Almacenar los vecinos descubiertos y sus conexiones
    topologia = defaultdict(list)
    for pkt in lldp_response:
        vecino = pkt[1][Ether].src
        puerto_local = pkt[0][Ether].src
        puerto_vecino = pkt[1][LLDP].tlvlist[1][1].decode()
        topologia[vecino].append((puerto_local, puerto_vecino))
    
    return topologia

def mostrar_topologia(topologia):
    for dispositivo, conexiones in topologia.items():
        print(f"Dispositivo: {dispositivo}")
        for conexion in conexiones:
            puerto_local, puerto_vecino = conexion
            print(f"  - Conectado al puerto {puerto_vecino} del dispositivo vecino a través del puerto {puerto_local}")

# Descubrir la topología de la red
topologia = descubrir_topologia()

# Mostrar la topología descubierta
mostrar_topologia(topologia)





