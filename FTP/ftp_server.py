import socket

HOST = '127.0.0.1'
PORT = 21

def iniciar_ftp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        
        print(f"--- Servidor Fake FTP corriendo en {HOST}:{PORT} ---")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"[{addr[0]}] Cliente conectado.")
            
            with client_socket:
                # 1. Saludo oficial de FTP (Código 220)
                client_socket.sendall(b"220 Bienvenido al Taller de Sockets FTP\r\n")
                
                # Variables de estado
                usuario_autenticado = False
                directorio_actual = "/home/lucas/taller"

                while True:
                    try:
                        datos = client_socket.recv(1024).decode('utf-8')
                        if not datos:
                            break
                    except:
                        break

                    # Limpiamos y separamos el comando de los argumentos (ej. "USER admin")
                    partes = datos.strip().split(" ", 1)
                    comando = partes[0].upper()
                    argumento = partes[1] if len(partes) > 1 else ""

                    print(f"Cliente: {comando} {argumento}")

                    # --- MÁQUINA DE ESTADOS FTP ---
                    
                    if comando == "USER":
                        # FTP siempre pide usuario primero
                        client_socket.sendall(b"331 Please specify the password.\r\n")
                        
                    elif comando == "PASS":
                        # Simulamos que cualquier contraseña es válida
                        usuario_autenticado = True
                        client_socket.sendall(b"230 Login successful.\r\n")
                        
                    elif comando == "SYST":
                        # El cliente pregunta qué sistema operativo usamos
                        client_socket.sendall(b"215 UNIX Type: L8\r\n")
                        
                    elif comando == "PWD":
                        # Print Working Directory
                        respuesta = f'257 "{directorio_actual}" is the current directory.\r\n'
                        client_socket.sendall(respuesta.encode('utf-8'))
                        
                    elif comando == "TYPE":
                        # El cliente avisa si mandará texto (A) o binario (I)
                        client_socket.sendall(b"200 Switching to Binary mode.\r\n")
                        
                    elif comando in ["PASV", "PORT", "LIST", "RETR"]:
                        # ¡Aquí está la lección! Explicar que esto requiere otro socket
                        client_socket.sendall(b"502 Command not implemented in this workshop (Requires Data Channel).\r\n")
                        
                    elif comando == "QUIT":
                        client_socket.sendall(b"221 Goodbye.\r\n")
                        break
                        
                    else:
                        client_socket.sendall(b"500 Unknown command.\r\n")

            print(f"[{addr[0]}] Cliente desconectado.\n")

if __name__ == '__main__':
    iniciar_ftp()