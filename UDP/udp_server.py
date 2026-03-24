import socket

HOST = '127.0.0.1'
PORT = 65432

print("--- SERVIDOR UDP ---")
print(f"Listo para recibir paquetes en {HOST}:{PORT}")

# 1. CREACIÓN DEL SOCKET
# socket.AF_INET   = Usamos IPv4
# socket.SOCK_DGRAM = Usamos UDP.
# EXPLICACIÓN: Datagrama es un paquete de datos autónomo.
# A diferencia del Stream, aquí no hay tubería continua. Recibimos paquetes sueltos.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    
    # 2. BIND (VINCULAR)
    # Necesario para que el sistema sepa a dónde dirigir los paquetes entrantes.
    server_socket.bind((HOST, PORT))
    
    # Acá NO hay listen() ni accept().
    # UDP no establece conexión. Simplemente espera a que le caiga algo.
    
    while True:
        # 3. RECVFROM
        # En UDP, como no hay conexión fija, cada paquete viene con la dirección del remitente.
        # recvfrom retorna:
        # - data: El contenido del mensaje.
        # - addr: La dirección de QUIÉN mandó este paquete específico.
        data, addr = server_socket.recvfrom(1024)
        
        message = data.decode('utf-8')
        print(f"Recibido mensaje de {addr}: {message}")
        
        # Procesamos
        response = message.upper()
        
        # 4. SENDTO
        # No podemos usar send a secas porque el socket no sabe con quién habla.
        # Debemos especificar la dirección (addr) explícitamente en cada mensaje.
        server_socket.sendto(response.encode('utf-8'), addr)