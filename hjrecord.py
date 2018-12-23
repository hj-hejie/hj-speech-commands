import pdb
import socketserver
import hjvad


class RecordServer(socketserver.BaseRequestHandler):

    def handle(self):
        frames = hjvad.socket_frame_generator(self.request)
        path='hjtest1.wav'
        buff=b''
        while True:
            cmd = input('cmd>')
            if cmd == 'r':
                for i, frame in enumerate(frames):
                    buff += frame.bytes
                    if i >= 99: break
                print('Recorded*********%s*********************************'%len(buff))
                hjvad.write_wave(path, buff, 1, 10000)
                buff=b''

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
