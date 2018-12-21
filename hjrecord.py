import pdb
import socketserver
import hjvad

path='hjtest1.wav'
buff=b''

class RecordServer(socketserver.BaseRequestHandler):

    def handle(self):
        frames = hjvad.socket_frame_generator(self.request)
        while True:
            cmd = input('cmd>')
            if cmd == 'r':
                for i, frame in enumerate(frames):
                    if i >= 100: break
                    buff += frame.bytes
                hjvad.write_wave(path, buff, 1, 10000)
            elif cmd == 't':
                print('hejie')

if __name__ == '__main__':
    try:
        print('Recordserver starting***********************************')
        server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),RecordServer)
        server.serve_forever()
        print('Recordserver started********************************')

    except KeyboardInterrupt:
        server.shutdown()
