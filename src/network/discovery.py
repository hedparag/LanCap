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
        import select
        sockets = []
        
        def setup_sockets():
            for s in sockets:
                try: s.close()
                except: pass
            sockets.clear()
            
            # 1. Bind to 0.0.0.0
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.bind(("", self.port))
                sockets.append(s)
            except Exception:
                pass
                
            # 2. Bind explicitly to each local IP to ensure Windows receives targeted UDP broadcasts
            try:
                ips = socket.gethostbyname_ex(self.system_name)[2]
                for ip in ips:
                    if ip.startswith("127."): continue
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        s.bind((ip, self.port))
                        sockets.append(s)
                    except Exception:
                        pass
            except Exception:
                pass

        setup_sockets()
        last_socket_setup = time.time()
        
        while self.running:
            current_time = time.time()
            if current_time - last_socket_setup > 15:
                # Refresh interfaces every 15 seconds
                setup_sockets()
                last_socket_setup = current_time
                
            if not sockets:
                time.sleep(1)
                continue
                
            try:
                readable, _, _ = select.select(sockets, [], [], 1.0)
                for sock in readable:
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
                            # Filter out ourselves
                            continue
                            
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
            except Exception:
                pass
                
            # Check for stale peers (not seen for 10 seconds)
            stale_ips = []
            for p_ip, p_data in self.peers.items():
                if current_time - p_data['last_seen'] > 10:
                    stale_ips.append(p_ip)
                    
            for stale_ip in stale_ips:
                del self.peers[stale_ip]
                self.peer_lost.emit(stale_ip)
                
        for s in sockets:
            try: s.close()
            except: pass

    def _broadcast_now(self):
        message = {
            'type': 'presence',
            'name': self.system_name,
            'status': self.status
        }
        data = json.dumps(message).encode('utf-8')
        
        # 1. Try general broadcast
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(data, ('<broadcast>', self.port))
            sock.close()
        except Exception:
            pass

        # 2. Try broadcasting specifically on all available network interfaces
        try:
            ips = socket.gethostbyname_ex(socket.gethostname())[2]
            for ip in ips:
                if ip.startswith("127."):
                    continue
                
                parts = ip.split('.')
                
                # Guess /24 broadcast address
                parts_24 = parts.copy()
                parts_24[3] = '255'
                bcast_24 = '.'.join(parts_24)
                
                # Guess /16 broadcast address
                parts_16 = parts.copy()
                parts_16[2] = '255'
                parts_16[3] = '255'
                bcast_16 = '.'.join(parts_16)
                
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                try:
                    # Bind to the specific interface adapter IP so Windows knows which NIC to send from
                    s.bind((ip, 0))
                    
                    # Target 255.255.255.255
                    s.sendto(data, ('<broadcast>', self.port))
                    
                    # Target explicit subnet broadcasts
                    s.sendto(data, (bcast_24, self.port))
                    s.sendto(data, (bcast_16, self.port))
                except Exception:
                    pass
                finally:
                    s.close()
        except Exception as e:
            pass
        
    def _broadcast_presence(self):
        while self.running:
            self._broadcast_now()
            # Broadcast every 3 seconds to ensure peers know we are here
            time.sleep(3)
