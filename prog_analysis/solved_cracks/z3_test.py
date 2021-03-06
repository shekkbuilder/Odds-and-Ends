from z3 import *
x86 = []
a = {}

def prePass():
	loops = []
	reg = None
	i = 0
	while(i < len(x86)):
		if x86[i][0] == 'jbe':
			count = x86[i-1][2]
			reg = x86[i-2][2]
			#print reg
			while(x86[i][1] != reg):
				loops.append(x86[i])
				i += 1
			loops.append(x86[i])
			loops = loops*(int(count)+1)
			loops.append(x86[len(x86)-1])
			
		i += 1

	if len(loops) > 0:
		return loops
	return x86
			

def parseReg(reg):
	if reg.isdigit():
		return
	elif reg not in a:
		x = BitVec(reg, 32)
		a.update({reg : x})

def parseInstruc(instruct):
	if "mov" in instruct:
		instruct = "mov"
	elif "imul" in instruct:
		instruct = "mul"
	elif "idiv" in instruct:
		instruct = "div"
	return instruct

def read_x86():
	print "ENTER FILE NAME"
	x = raw_input("> ")
	fin = file(x).readlines()
	for i in fin:
		i = i.replace("[","")
		i = i.replace("]","")
		i = i.replace(",","")
		i = i.replace("\n","")
		i = i.replace("    ","")
		i = i.split(" ")
		i[0] = parseInstruc(i[0])
		parseReg(i[1])
		parseReg(i[2])
		x86.append(i)

def mov_const(x, solver):
	if x[2].isdigit():
		a[x[1]] = int(x[2])
	else:
		a[x[1]] = a[x[2]]

def cmp_const(x, solver):
	if x[2].isdigit():
		#print a[x[1]], a[x[2]]
		solver.add(a[x[1]] == x[2])
	else:
		print a[x[1]], a[x[2]]
		solver.add(a[x[1]] == a[x[2]])

def add_const(x,solver):
	if x[2].isdigit():
		a[x[1]] += int(x[2])
	else:
		a[x[1]] += a[x[2]]

def sub_const(x,solver):
	if x[2].isdigit():
		a[x[1]] -= int(x[2])
	else:
		a[x[1]] -= a[x[2]]

def xchg_const(x,solver):
	a[x[1]] = a[x[2]]

def shl_const(x,solver):
	a[x[1]] = (a[x[1]] << int(x[2]))

def shr_const(x,solver):
	a[x[1]] = (a[x[1]] >> int(x[2]))

def mul_const(x,solver):
	if x[2].isdigit():
		a[x[1]] *= int(x[2])
	else:
		a[x[1]] *= a[x[2]]

def xor_const(x,solver):
	if x[2].isdigit():
		a[x[1]] = a[x[1]] ^ int(x[2])
	else:
		a[x[1]] = a[x[1]] ^ a[x[2]]

def div_const(x,solver):
	if x[2].isdigit():
		a[x[1]] = a[x[1]] / int(x[2])
	else:
		a[x[1]] = a[x[1]] / a[x[2]]
	
def develop_const(x,solver):
	if x[0] == 'mov':
		mov_const(x,solver)
	elif x[0] == 'cmp':
		cmp_const(x,solver)
	elif x[0] == 'jbe':
		return
	elif x[0] == 'jmp':
		return
	elif x[0] == 'nop':
		return
	elif x[0] == 'call':
		return
	elif x[0] == 'add':
		add_const(x,solver)
	elif x[0] == 'sub':
		sub_const(x,solver)
	elif x[0] == 'xchg':
		xchg_const(x,solver)
	elif x[0] == 'shl':
		shl_const(x,solver)
	elif x[0] == 'shr':
		shr_const(x,solver)
	elif x[0] == 'xor':
		xor_const(x,solver)
	elif x[0] == 'lea':
		mov_const(x,solver)
	elif x[0] == 'mul':
		mul_const(x,solver)
	elif x[0] == 'div':
		div_const(x,solver)
	else:
		print "UNSUPPORTED OPERATION {0}".format(x[0])
		#exit()

def main():
	read_x86()
	x86 = prePass()

	#print "\n", x86
	s = Solver()
	#init_registers()
	for i in x86:
		develop_const(i,s)

	#print x86
	print s
	a = str(s.check())
	if a == "sat":
		print s.model()
	

main()

