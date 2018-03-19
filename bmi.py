#!/usr/bin/env python3
import argparse, socket
from datetime import datetime
import time

MAX_BYTES = 65535

def server(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host, port))
	print('Listening at {}'.format(sock.getsockname()))
	while True:
		data, address = sock.recvfrom(MAX_BYTES)
		text = data.decode('ascii')
		print('The client at {} says {!r}'.format(address, text))

		try:
			text = text.split()
			height = float(text[0])
			weight = float(text[1])
			response = "Your BMI is "+str(round(weight/height/height, 2));
		except Exception as e:
			response = "Something went wrong"
		else:
			pass
		finally:
			pass
		
		data = response.encode('ascii')
		sock.sendto(data, address)

def client(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	height = input("Input your height (m):")
	weight = input("Input your weight (kg):")

	text = height+' '+weight
	data = text.encode('ascii')

	start = time.time()

	sock.sendto(data, (host, port))
	data, address = sock.recvfrom(MAX_BYTES)

	duration = time.time()-start

	text = data.decode('ascii')
	print(text, "spend "+str(round(duration, 2))+" seconds")

if __name__ == '__main__':
	choices = {'client': client, 'server': server}
	parser = argparse.ArgumentParser(description='Send and receive UDP locally')
	parser.add_argument('role', choices=choices, help='which role to play')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060,
						help='UDP port (default 1060)')
	parser.add_argument('--host', metavar='HOST', type=str, default='127.0.01',
						help='Host (default 127.0.0.1)')
	args = parser.parse_args()
	function = choices[args.role]
	function(args.host, args.p)
