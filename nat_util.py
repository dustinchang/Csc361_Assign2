import copy

'''
purpose
	return True if s is a string consisting of an integer in [low..high]
preconditions
	s is a string
	low, high are integers
'''
def int_in_range(s,low,high):
	try:
		n = int(s)
		if low <= n and n <= high:
			return True
		else:
			return False
	except:
		return False


'''-----------------------------------------------------------------
purpose
	return True if p is a string consisting of an integer in [1..2**16-1]
preconditions
	p is a string
'''
def legal_port(p):
	return int_in_range(p,1,2**16-1)


'''-----------------------------------------------------------------
purpose
	return True if a is a string consisting of a dotted decimal address
	with each field in [0..255]
preconditions
	a is a string
'''
def legal_address(a):
	try:
		x = a.split('.')
		if len(x) != 4:
			return False
		for i in x:
			if not int_in_range(i,0,2**8-1):
				return False
		return True
	except:
		return False


'''-----------------------------------------------------------------
purpose
	return True if t is a list consisting of a legal 5-tuple:
		[ protocol, src_ip, src_port, dst_ip, dst_port]
	where
		protocol is 'tcp' or 'udp'
		src_ip and dst_ip are IP addresses
		src_port and dst_port are tcp or udp ports
preconditions
	none
'''
def legal_5_tuple(t):
	if \
	 type(t) == list and len(t) == 5 and \
	 t[0] in ['tcp','udp'] and \
	 legal_address(t[1]) and \
	 legal_port(t[2]) and \
	 legal_address(t[3]) and \
	 legal_port(t[4]):
		return True
	else:
		return False

'''-----------------------------------------------------------------
purpose
	return a tuple (T,C) where
		T is a copy of the input with 'accept' or 'drop' appended
			to each item
		C is the resulting connection tracking table, with each row
			consisting of two items:
			a private 5-tuple and a public 5-tuple
preconditions
	traffic_list is a list of [T,direction] where
		T is a 5-tuple and direction is 'inbound' or 'outbound'
'''
#makeC function was added by us
# input private list, output public/private list
def makeC(traffic_line, public_addr, nat_port):
	trafcpy = list(traffic_line)
	Clist = [traffic_line, trafcpy]
	Clist[1][1] = public_addr
	Clist[1][2] = str(nat_port)
	return Clist

def generate_tables(traffic_list, public_address, nat_port):
	T = []
	C = []
	for p in traffic_list:
		pcpy = copy.copy(p)
		if pcpy[1] == 'outbound':
			outFlag = False
			pcpy.append('accept')
			T.append(pcpy)
			#C empty
			if not C:
				C.append(makeC(pcpy[0], public_address, nat_port))
				nat_port = int(nat_port)
				nat_port = nat_port + 1
			else:				
				for k in C:
					if pcpy[0] == k[0]:
						print 'EQUAL'
						outFlag = True
				if not outFlag:
					print 'NOT EQUAL'
					C.append(makeC(pcpy[0], public_address, nat_port))
					nat_port = int(nat_port)
					nat_port = nat_port + 1
		#pcpy[1] == 'inbound'
		else: 
			#C empty - drop by default
			inFlag = False
			if not C:
				pcpy.append('drop')
				T.append(pcpy)
			else:
				for k in C:
					#check if packet in list - P.destAddr == C.public.sourceAddr and 
					#p.destPort = C.public.sourcePort
					inDestAddr = pcpy[0][3]
					inDestPort = pcpy[0][4]
					outPubSrcAddr = k[1][1]
					outPubSrcPort = k[1][2]
					if((inDestAddr==outPubSrcAddr) and (inDestPort==outPubSrcPort)):
						pcpy.append('accept')
						T.append(pcpy)	
						inFlag = True
				if not inFlag:
					pcpy.append('drop')
					T.append(pcpy) 
		#print "T: "
		#print T
		#print "C: "
		#print C
	return (T, C)
