from netmiko import ConnectHandler
import re
# Definir los detalles de conexión SSH
def discover():
    device = {
        'device_type': 'cisco_ios',
        'ip': '192.168.1.1',  # Reemplaza con la dirección IP de tu dispositivo
        'username': 'gmedina',  # Reemplaza con tu nombre de usuario SSH
        'password': 'cisco',  # Reemplaza con tu contraseña SSH
    }

    # Iniciar la conexión SSH
    ssh_connection = ConnectHandler(**device)

    # Comando de ejemplo para cambiar el banner de inicio
    new_banner = " & Bienvenido al router modificado por el script de Ramon,yarib y Arseniy. &"
    banner_command = f"banner login {new_banner}"

    # Comando de ejemplo para cambiar el hostname
    new_hostname = "switch,ramon,yarib,arseniy"
    hostname_command = f"hostname {new_hostname}"

    # Lista de comandos a enviar
    config_commands = [ banner_command,hostname_command]

    # Enviar los comandos de configuración
    output = ssh_connection.send_config_set(config_commands)

    # Mostrar la salida de la configuración aplicada
    print("Salida de la configuración aplicada: ")
    print(output)

    cdp_neighbors_output =ssh_connection.send_command("show cdp neighbors")
    print("Salida")
    print(cdp_neighbors_output)
    # Cerrar la conexión SSH
    ssh_connection.disconnect()

    neighbors_info = []

    # Separar la salida por líneas
    output_lines = cdp_neighbors_output.split('\n')

    # Banderas para controlar dónde comienza y termina la información importante
    start_parsing = False

    # Procesar cada línea para extraer datos
    for line in output_lines:
        if line.strip().startswith("Device ID"):  # Determina el comienzo de la tabla de datos
            start_parsing = True
            continue

        if start_parsing:
            # Analizar línea para obtener información relevante (se espera formato tabulado)
            # Este patrón de expresiones regulares busca valores separados por uno o más espacios
            match = re.split(r'\s{2,}', line.strip())
            
            if len(match) >= 5:  # Verificar que haya suficiente información en la línea
                device_id = match[0]
                local_interface = match[1]
                port_id = match[4]
                
                # Agregar información a la lista
                neighbors_info.append({
                    'device_id': device_id,
                    'local_interface': local_interface,
                    'port_id': port_id
                })

    # Mostrar la información procesada
    print("Información de vecinos CDP:")
    for info in neighbors_info:
        print(f"Dispositivo: {info['device_id']}, Interfaz local: {info['local_interface']}, Interfaz remota: {info['port_id']}")

