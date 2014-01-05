import os
import socket
import random
from peer import *


def check_finger_table_integrity(id, finger_table, hash_list):
	print "checking the finger table integrity of %s" % id
	for i in range(0, LOGSIZE):
		finger_id = finger_table[i].id()
		# finger_id is in [id + 2^i, id)
		assert inrange(finger_id, (id + (1<<i)) % SIZE, id)
		for j in range(0, len(hash_list)):
			if (hash_list[j] == finger_id):
				continue
			# there's no other finger in between
			assert (id + (1<<i)) % SIZE == finger_id or not inrange(hash_list[j], (id + (1<<i)) % SIZE, finger_id)

# create addresses
address_list = map(lambda addr: Address('127.0.0.1', addr), range(10100, 10400, 7))
# keep unique ones
address_list = sorted(set(address_list))
# hash the addresses
hash_list 	 = map(lambda addr: addr.__hash__(), address_list)
# create the nodes
locals_list   = []
for i in range(0, len(address_list)):
	try:
		if len(locals_list) == 0:
			local = Local(address_list[i])
		else:
			# use a random already created peer's address
			# as a remote
			local = Local(address_list[i], locals_list[random.randrange(len(locals_list))].address_)
		locals_list.append(local)
	except Exception:
		pass

print "done creating peers, our pid %s is" % os.getpid()
hash_list.sort()

# check integrity
for local in locals_list:
	check_finger_table_integrity(local.id(), local.finger_, hash_list)

# shutdown peers
for local in locals_list:
	msocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	msocket.connect((local.address_.ip, local.address_.port))
	msocket.sendall('shutdown')
	msocket.close()