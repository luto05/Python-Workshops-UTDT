import socket

HOST = '127.0.0.1'
PORT = 25

def iniciar_smtp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        
        print(f"--- Servidor Fake SMTP corriendo en {HOST}:{PORT} ---")
        print("Esperando que alguien envíe un correo...\n")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"[{addr[0]}] Cliente conectado.")
            
            with client_socket:
                # 1. El servidor saluda primero (Código 220)
                client_socket.sendall(b"220 Bienvenido al Taller SMTP de Python\r\n")
                
                en_modo_datos = False
                cuerpo_mensaje = ""

                while True:
                    # 2. Leer lo que dice el cliente
                    try:
                        datos = client_socket.recv(1024).decode('utf-8')
                        if not datos:
                            break
                    except:
                        break

                    # Limpiamos los saltos de línea para leer el comando
                    comando_limpio = datos.strip()
                    print(f"Cliente dice: {comando_limpio}")

                    # 3. MÁQUINA DE ESTADOS (Procesar los comandos SMTP)
                    
                    if en_modo_datos:
                        # Si estamos en modo DATA, todo lo que llega es el cuerpo del mail
                        # El estándar dice que el mail termina cuando llega un punto solo en una línea (".\r\n")
                        if comando_limpio == ".":
                            en_modo_datos = False
                            print("\n--- NUEVO CORREO RECIBIDO ---")
                            print(cuerpo_mensaje)
                            print("-----------------------------\n")
                            client_socket.sendall(b"250 OK: Correo aceptado para entrega\r\n")
                            cuerpo_mensaje = "" # Limpiamos para el próximo mail
                        else:
                            cuerpo_mensaje += datos # Acumulamos el texto
                            
                    else:
                        # Convertimos a mayúsculas para comparar fácil (ej. helo -> HELO)
                        comando_base = comando_limpio.upper()

                        if comando_base.startswith("HELO") or comando_base.startswith("EHLO"):
                            client_socket.sendall(b"250 OK Hello encantado de conocerte\r\n")
                            
                        elif comando_base.startswith("MAIL FROM:"):
                            client_socket.sendall(b"250 OK Sender accepted\r\n")
                            
                        elif comando_base.startswith("RCPT TO:"):
                            client_socket.sendall(b"250 OK Recipient accepted\r\n")
                            
                        elif comando_base == "DATA":
                            # Le decimos al cliente que empiece a escribir y cómo terminar (con un punto)
                            client_socket.sendall(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
                            en_modo_datos = True
                            
                        elif comando_base == "QUIT":
                            client_socket.sendall(b"221 Bye. Cerrando conexion\r\n")
                            break # Salimos del bucle interno y cerramos conexión
                            
                        else:
                            # Si manda un comando que no conocemos
                            client_socket.sendall(b"500 Comando no reconocido\r\n")

            print(f"[{addr[0]}] Cliente desconectado.\n")

if __name__ == '__main__':
    iniciar_smtp()