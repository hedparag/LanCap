import socket
import threading
import json
from PySide6.QtCore import QObject, Signal

class MessageService(QObject):
    message_received = Signal(str, str) # ip, message_text

    def __init__(self, port=37021):
        super().__init__()
        self.port = port
        self.running = False
        
    def start(self):
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen_for_messages, daemon=True)
        self.listen_thread.start()
        
    def stop(self):
        self.running = False
        
    def _listen_for_messages(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", self.port))
            sock.listen(5)
            sock.settimeout(1.0)
        except OSError as e:
            print(f"Failed to bind messaging port {self.port}: {e}")
            return
            
        while self.running:
            try:
                conn, addr = sock.accept()
                threading.Thread(target=self._handle_connection, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                pass
            except Exception as e:
                pass
                
        sock.close()
        
    def _handle_connection(self, conn, addr):
        ip = addr[0]
        try:
            data = conn.recv(4096)
            if data:
                message = json.loads(data.decode('utf-8'))
                if message.get('type') == 'chat':
                    text = message.get('text', '')
                    self.message_received.emit(ip, text)
        except Exception as e:
            pass
        finally:
            conn.close()
            
    def send_message(self, ip, text):
        def _send():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5.0)
                sock.connect((ip, self.port))
                
                message = {
                    'type': 'chat',
                    'text': text
                }
                data = json.dumps(message).encode('utf-8')
                sock.sendall(data)
                sock.close()
                return True
            except Exception as e:
                print(f"Failed to send to {ip}: {e}")
                return False
                
        # Send immediately in a thread to avoid blocking UI
        threading.Thread(target=_send, daemon=True).start()
