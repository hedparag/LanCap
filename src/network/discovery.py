import socket
import threading
import json
import time
from PySide6.QtCore import QObject, Signal

class PeerDiscovery(QObject):
    peer_discovered = Signal(str, str, str) # ip, name, status
    peer_lost = Signal(str) # ip

    def __init__(self, port=37020):
        super().__init__()
        self.port = port
        self.system_name = socket.gethostname()
        self.peers = {} # ip -> {'name': name, 'status': status, 'last_seen': timestamp}
        self.running = False
        self.status = "Available"
        
    def start(self):
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen_for_broadcasts, daemon=True)
        self.listen_thread.start()
        
        self.broadcast_thread = threading.Thread(target=self._broadcast_presence, daemon=True)
        self.broadcast_thread.start()

    def set_status(self, status):
        self.status = status
        # Trigger an immediate broadcast when status changes
        self._broadcast_now()

    def stop(self):
        self.running = False

    def _listen_for_broadcasts(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        
        # Allow multiple sockets to bind to this port
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass
            
        # Bind
        try:
            sock.bind(("", self.port))
        except OSError as e:
            print(f"Failed to bind discovery port {self.port}: {e}")
            return
            
        sock.settimeout(1.0)
        
        # Get own IP addresses to avoid self-discovery
        own_ips = set()
        try:
            own_ips = set(socket.gethostbyname_ex(self.system_name)[2])
        except:
            pass
        own_ips.add('127.0.0.1')
        
        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                ip = addr[0]
                
                try:
                    message = json.loads(data.decode('utf-8'))
                except:
                    continue
                    
                if message.get('type') == 'presence':
                    name = message.get('name')
                    status = message.get('status', 'Available')
                    
                    if name == self.system_name: 
                        # Filter out ourselves (same host)
                        continue
                        
                    current_time = time.time()
                    
                    is_new_or_updated = False
                    if ip not in self.peers:
                        is_new_or_updated = True
                    elif self.peers[ip]['name'] != name or self.peers[ip]['status'] != status:
                        is_new_or_updated = True
                        
                    self.peers[ip] = {
                        'name': name,
                        'status': status,
                        'last_seen': current_time
                    }
                    
                    if is_new_or_updated:
                        self.peer_discovered.emit(ip, name, status)
                        
            except socket.timeout:
                pass
            except Exception as e:
                pass
                
            # Check for stale peers (not seen for 10 seconds)
            current_time = time.time()
            stale_ips = []
            for p_ip, p_data in self.peers.items():
                if current_time - p_data['last_seen'] > 10:
                    stale_ips.append(p_ip)
                    
            for stale_ip in stale_ips:
                del self.peers[stale_ip]
                self.peer_lost.emit(stale_ip)
                
        sock.close()
        
    def _broadcast_now(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        message = {
            'type': 'presence',
            'name': self.system_name,
            'status': self.status
        }
        data = json.dumps(message).encode('utf-8')
        try:
            sock.sendto(data, ('<broadcast>', self.port))
        except Exception as e:
            pass
        sock.close()
        
    def _broadcast_presence(self):
        while self.running:
            self._broadcast_now()
            # Broadcast every 3 seconds to ensure peers know we are here
            time.sleep(3)
