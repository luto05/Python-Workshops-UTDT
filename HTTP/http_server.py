import socket

# Configuración del servidor
HOST = '127.0.0.1'  # Localhost
PORT = 80           # Puerto para HTTP

def iniciar_servidor():
    # 1. Crear el socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        
        # Esto evita el error "Address already in use" si reinicias el script rápido
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 2. Vincular y Escuchar
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"--- Servidor Web corriendo en http://{HOST}:{PORT} ---")
        print("Esperando conexiones de navegadores...\n")

        while True:
            # 3. Aceptar la conexión del cliente (El navegador)
            client_socket, addr = server_socket.accept()
            
            with client_socket:
                # 4. Leer la petición
                # Recibimos hasta 1024 bytes de texto y lo decodificamos
                request_data = client_socket.recv(1024).decode('utf-8')
                
                # Imprimimos lo que el navegador nos mandó
                print(f"[{addr[0]}] Petición recibida:")
                print("-" * 20)
                print(request_data)
                print("-" * 20)

                # 5. Construir la respuesta
                # Regla de HTTP: Los Headers y el Body se separan por una línea en blanco (\r\n\r\n)
                
                # HEADERS: Le decimos al navegador "Todo OK, te mando un HTML"
                headers = "HTTP/1.1 200 OK\r\n"
                headers += "Content-Type: text/html; charset=utf-8\r\n"
                headers += "Connection: close\r\n\r\n" # La línea en blanco crucial
                
                # BODY: El código HTML real
                body = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Mi Servidor Python</title>
                    <style>
                        body { font-family: monospace; background-color: #222; color: #0f0; padding: 50px; }
                        h1 { color: #fff; }
                    </style>
                </head>
                <body>
                    <h1>¡Hola desde Sockets Crudos!</h1>
                    <p>Si estás viendo esto, tu servidor HTTP funciona perfectamente.</p>
                </body>
                </html>
                """

                # 6. Enviar todo junto al navegador
                http_response = headers + body
                client_socket.sendall(http_response.encode('utf-8'))
                
            # Al salir del bloque 'with client_socket', la conexión se cierra automáticamente (Enviando el paquete FIN)

if __name__ == '__main__':
    iniciar_servidor()