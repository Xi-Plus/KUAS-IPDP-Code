#!/usr/bin/env python3
import argparse, socket
import re
import random
import time

MAX_BYTES = 65535

def server(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host, port))
	print('Listening at {}'.format(sock.getsockname()))

	answer = {}
	count = {}
	while True:
		data, address = sock.recvfrom(MAX_BYTES)
		text = data.decode('ascii')

		print('The client at {} says {!r}'.format(address, text))

		try:
			if len(text) != 4:
				raise

			if re.match(r"^\d{4}$", text) == None:
				raise

			key = str(address)

			if key not in answer:
				answer[key] = ""
				count[key] = 0
				for i in range(4):
					c = str(random.randint(0, 9))
					while c in answer[key]:
						c = str(random.randint(0, 9))
					answer[key] += c

			count[key] += 1
			print(key, answer[key])

			A = 0
			B = 0
			for i in range(4):
				for j in range(4):
					if text[i] == answer[key][j]:
						if i == j:
							A += 1
						else :
							B += 1

			if A == 4:
				response = f"4A. Your answer is correct. Spend {count[key]} times."
				del answer[key]
			else :
				response = f"{A}A{B}B"

		except Exception as e:
			response = "Wrong input"
		else:
			pass
		finally:
			pass
		
		data = response.encode('ascii')
		sock.sendto(data, address)

def client(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.connect((host, port))

	while True:
		text = input("Input your answer:")
		data = text.encode('ascii')
		start = time.time()

		sock.send(data)
		data = sock.recv(MAX_BYTES)

		duration = time.time()-start

		text = data.decode('ascii')

		print(text+" (spend "+str(round(duration, 2))+" seconds)")

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
