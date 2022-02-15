import socket, cv2, pickle, struct
from threading import Thread

SERVER = 'localhost'
PORT = 5454

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER,PORT))
server.listen()
print(f"[LISTENING] Server is listening on {SERVER}")

connection, address = server.accept()
print(f"[NEW CONNECTION] New Connection : {connection} | ADDR : {address} connected.")

class StreamVideo(Thread):
    def run(self):
        while True:
            video = cv2.VideoCapture(0)
            Img,Frame = video.read()
            data = pickle.dumps(Frame)
            msg = struct.pack('Q',len(data)) + data
            connection.send(msg)
            cv2.imshow('Server Sending...', Frame)
            
            if cv2.waitKey(13) == ord('q'):
                cv2.destroyAllWindows()
                server.close()
                    
class ReceiveVideo(Thread):
    def run(self):
        data = b''
        payload = struct.calcsize("Q") #bytes
        while True:
            while len(data) < payload:
                packet = connection.recv(3*1024) #2kB
                if not packet:
                    break
                data += packet
            PackedMsg = data[:payload]        
            data = data[payload:]
            msg = struct.unpack("Q", PackedMsg)[0]
            
            while len(data) < msg :
                data += connection.recv(3*1024)
                
            FrameData = data[:msg]
            data = data[msg:]
            frame = pickle.loads(FrameData)
            
            cv2.imshow('Server Receiving..,',frame)
            if cv2.waitKey(10) == ord('q'):
                server.close()
            
StreamVideo().start()
ReceiveVideo().start()
