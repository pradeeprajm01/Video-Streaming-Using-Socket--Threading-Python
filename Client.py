import socket, cv2, struct, pickle, imutils
from threading import Thread

SERVER = 'localhost'
PORT = 5454

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER,PORT))
print(f"[CONNECTED] Connecting to {SERVER}")

class StreamVideo(Thread):
    def run(self):
        while True:
            video = cv2.VideoCapture(0)
            Img,Frame = video.read()
            data = pickle.dumps(Frame)
            msg = struct.pack('Q',len(data)) + data
            client.send(msg)
            cv2.imshow('Client Sending...', Frame)
            
            if cv2.waitKey(13) == ord('q'):
                cv2.destroyAllWindows()
                server.close()
                    
class ReceiveVideo(Thread):
    def run(self):
        data = b''
        payload = struct.calcsize("Q") #bytes
        while True:
            while len(data) < payload:
                packet = client.recv(3*1024) #2kB
                if not packet:
                    break
                data += packet
            PackedMsg = data[:payload]        
            data = data[payload:]
            msg = struct.unpack("Q", PackedMsg)[0]
            
            while len(data) < msg :
                data += client.recv(3*1024)
                
            FrameData = data[:msg]
            data = data[msg:]
            frame = pickle.loads(FrameData)
            
            cv2.imshow('Client Receiving..,',frame)
            if cv2.waitKey(10) == ord('q'):
                client.close()
            
StreamVideo().start()
ReceiveVideo().start()