import getopt, sys
from prettytable import PrettyTable
from collections import OrderedDict

def eprint(arg):
	print >> sys.stderr, arg

def usage_config():
	print "config command usage"
	print "command arguments: aggiestack config "
	print "positional arguments:"
	print "--hardware\t\tRead the hardware configuration file"
	print "--images\t\tRead the images configuration file"
	print "--flavors\t\tRead the flavor instances configuration file"

def usage_show():
	print "show command usage"
	print "command arguments: "
	print "aggiestack show hardware\tList the hardware information"
	print "aggiestack show images\t\tList the images information"
	print "aggiestack show flavors\t\tList the flavor information"
	print "aggiestack show all\t\tList all the information"

def usage():
	usage_config()
	usage_show()

def show_all():
	HW.show()
	IMG.show()
	FLV.show()

class Hardware:
	def __init__(self):
		self.hw_list = OrderedDict();
		self.hw_attr_list = ["name", "ip", "mem", "num-disk", "num-vcpus"]
	def insert(self, hw_inst):
		hw_dict = OrderedDict()
		hw_dict["name"] = hw_inst[0]
		hw_dict["ip"] = hw_inst[1]
		hw_dict["mem"] = int(hw_inst[2])
		hw_dict["num-disk"] = int(hw_inst[3])
		hw_dict["num-vcpus"] = int(hw_inst[4])
		self.hw_list[hw_dict["name"]] = hw_dict
	def get_machine(self, machine_name):
		return self.hw_list[machine_name]
	def get_machine_list(self):
		return self.hw_list.keys()
	# alloc resources flavor requires from a machine
	def alloc(self, machine, flavor):
		alloc_list = ["mem", "num-disk", "num-vcpus"]
		for i in alloc_list:
			self.hw_list[machine][i] -= flavor[i]
	# release resources flavor requires from a machine
	def release(self, machine, flavor):
		release_list = ["mem", "num-disk", "num-vcpus"]
		for i in release_list:
			self.hw_list[machine][i] += flavor[i]
	def show(self):
		t = PrettyTable(self.hw_attr_list)
		for k, v in self.hw_list.items():
			t.add_row(v.values())
		print t

class Images:
	def __init__(self):
		self.img_list = OrderedDict()
		self.img_attr_list = ["image-name", "path"]
	def insert(self,img_inst):
		img_dict = OrderedDict()
		img_dict["image-name"] = img_inst[0]
		img_dict["path"] = img_inst[1]
		self.img_list[img_dict["image-name"]] = img_dict
	def get_image(self, image_name):
		return self.img_list[image_name]
	def show(self):
		t = PrettyTable(self.img_attr_list)
		for k, v in self.img_list.items():
			t.add_row(v.values())
		print t

class Flavors:
	def __init__(self):
		self.flv_list = OrderedDict()
		self.flv_attr_list = ["type", "mem", "num-disk", "num-vcpus"]
	def insert(self,flv_inst):
		flv_dict = OrderedDict() 
		flv_dict["type"] = flv_inst[0]
		flv_dict["mem"] = int(flv_inst[1])
		flv_dict["num-disk"] = int(flv_inst[2])
		flv_dict["num-vcpus"] = int(flv_inst[3])
		self.flv_list[flv_dict["type"]] = flv_dict
	def get_flavor(self, flavor_name):
		return self.flv_list[flavor_name]
	def show(self):
		t = PrettyTable(self.flv_attr_list)
		for k, v in self.flv_list.items():
			t.add_row(v.values())
		print t

class Instance:
	def __init__(self):
		self.inst_list = OrderedDict()
		self.inst_attr_list = ["name", "machine", "image", "flavor"]
	def add(self, inst):
		inst_dict = OrderedDict() 
		inst_dict["name"] = inst[0]
		inst_dict["machine"] = inst[1]
		inst_dict["image"] = inst[2]
		inst_dict["flavor"] = inst[3]
		self.inst_list[inst_dict["name"]] = inst_dict
	def get_instance(self, inst_name):
		return self.inst_list.get(inst_name)
	def remove(self, inst_name):
		self.inst_list.pop(inst_name, None)
	def list(self):
		list_attr = list(self.inst_attr_list)
		list_attr.remove("machine")
		t = PrettyTable(list_attr)
		for k, v in self.inst_list.items():
			row = [v[x] for x in list_attr]
			t.add_row(row)
		print t
	def show_instance(self):
		list_attr = ["name", "machine"]
		print_list_attr = ["instance name", "physical server"]
		t = PrettyTable(print_list_attr)
		for k, v in self.inst_list.items():
			row = [v[x] for x in list_attr]
			t.add_row(row)
		print t

def do_config(option,arg):
	try:
		f = open(arg, 'r')
	except:
		eprint("No such file: "+arg)
		exit(0)
	if option == "--hardware":
		num_of_line = f.readline()
		for i in xrange(int(num_of_line)):
			hw_inst = f.readline()
			hw_inst = hw_inst.split()
			HW.insert(hw_inst)
			HW_free.insert(hw_inst)
	elif option == "--images":
		num_of_line = f.readline()
		for i in xrange(int(num_of_line)):
			img_inst = f.readline()
			img_inst = img_inst.split()
			IMG.insert(img_inst)
	elif option == "--flavors":
		num_of_line = f.readline()
		for i in xrange(int(num_of_line)):
			flv_inst = f.readline()
			flv_inst = flv_inst.split()
			FLV.insert(flv_inst)

def check_can_host(machine, flavor):
	m_inst = HW_free.get_machine(machine)
	f_inst = FLV.get_flavor(flavor)
	check_list = ["mem", "num-disk", "num-vcpus"]
	can_host = True
	for i in check_list:
		if int(f_inst[i]) > int(m_inst[i]):
			can_host = False
			break;
	return can_host

def server_create(name, image, machine, flavor_type):
	flavor = FLV.get_flavor(flavor_type)
	HW_free.alloc(machine, flavor)
	inst = [name, machine, image, flavor_type]
	INST.add(inst)

def server_delete(name):
	inst = INST.get_instance(name)
	if inst is None:
		return False
	machine = inst["machine"];
	flavor = FLV.get_flavor(inst["flavor"])
	HW_free.release(machine, flavor)
	INST.remove(name)
	return True

HW=Hardware()
HW_free=Hardware()
IMG=Images()
FLV=Flavors()
INST=Instance()

def main():
	while True:
		argv = raw_input('> ')
		argv = argv.split();
		try:
			program_name = argv[0]
		except:
			usage()

		# valid test
		if program_name == "q" or program_name == "quit":
			exit(0)
		elif program_name != "aggiestack":
			usage()
			continue
		try:
			issuer = argv[1]
			if issuer != "admin" and issuer != "server":
				issuer = None
				cmd = argv[1]
			else:
				cmd = argv[2]
		except:
			usage()
			continue

		if issuer is None:
			if cmd == "config":
				try:
					opts, args = getopt.getopt(argv[2:], "h", ["hardware=", "images=", "flavors="])
				except getopt.GetoptError as err:
					eprint(str(err))  # will print something like "option -a not recognized"
					usage_config()
				if len(opts) == 0:
					usage_config()
				for o, a in opts:
					if o == "--hardware" or o == "--images" or o == "--flavors":
						do_config(o,a)
					else:
						usage_config()

			elif cmd == "show":
				try:
					cmd = argv[2]
					if cmd == "hardware":
						HW.show()
					elif cmd == "images":
						IMG.show()
					elif cmd == "flavors":
						FLV.show()
					elif cmd == "all":
						show_all()
					else:
						usage_show()
				except:
					usage_show()
		elif issuer == "admin":
			if cmd == "show":
				try:
					suffix = argv[3]
					if suffix == "hardware":
						HW_free.show()
					elif suffix == "instance":
						INST.show_instance()
					else:
						usage_show()
				except:
					usage_show()	
			elif cmd == "can_host":
				try:
					machine_name = argv[3]
					flavor_type = argv[4]
					print check_can_host(machine_name, flavor_type)
				except:
					usage_show()

		elif issuer == "server":
			if cmd == "create":
				try:
					opts, args = getopt.getopt(argv[3:], "h", ["image=", "flavor=", "instance_name"])
				except getopt.GetoptError as err:
					eprint(str(err))  # will print something like "option -a not recognized
				if len(opts) != 2 or args is None:
					usage_show()
				for o, a in opts:
					if o == "--image":
						image = a
					if o == "--flavor":
						flavor_type = a
				inst_name = args[0]
				machine_list = HW_free.get_machine_list()
				create_success = False
				for i in machine_list:
					# simple first fit algorithm, can be further improved
					if check_can_host(i, flavor_type) == True:
						server_create(inst_name, image, i, flavor_type)
						create_success = True
						break
				if create_success == False:
					eprint("No more available resources")
			elif cmd == "delete":
				inst_name = argv[3]
				if server_delete(inst_name) == False:
					err = inst_name + " instance not exist!"
					eprint(err)
			elif cmd == "list":
				INST.list()


if __name__ == "__main__":
    main()
