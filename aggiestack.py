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

def show_hardware():
	HW.show()

def show_images():
	IMG.show()

def show_flavors():
	FLV.show()

def show_all():
	show_hardware()
	show_images()
	show_flavors()

class Hardware:
	def __init__(self):
		self.hw_list = OrderedDict();
		self.hw_attr_list = ["name", "ip", "mem", "num-disk", "num-vcpus"]
	def insert(self, hw_inst):
		hw_dict = OrderedDict();
		hw_dict["name"] = hw_inst[0];
		hw_dict["ip"] = hw_inst[1];
		hw_dict["mem"] = hw_inst[2];
		hw_dict["num-disk"] = hw_inst[3];
		hw_dict["num-vcpus"] = hw_inst[4];
		self.hw_list[hw_dict["name"]] = hw_dict
	def get_machine(self, machine_name):
		return hw_list[machine_name]
	def show(self):
		try:
			t = PrettyTable(self.hw_attr_list)
		except:
			print "No hardware information yet"
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
	def show(self):
		try:
			t = PrettyTable(self.img_attr_list)
		except:
			print "No images information yet"
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
		flv_dict["mem"] = flv_inst[1]
		flv_dict["num-disk"] = flv_inst[2]
		flv_dict["num-vcpus"] = flv_inst[3]
		self.flv_list[flv_dict["type"]] = flv_dict
	def show(self):
		try:
			t = PrettyTable(self.flv_attr_list)
		except:
			print "No flavors information yet"
		for k, v in self.flv_list.items():
			t.add_row(v.values())
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
	m_inst = HW.get_machine(machine)


HW=Hardware()
IMG=Images()
FLV=Flavors()

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
						show_hardware()
					elif cmd == "images":
						show_images()
					elif cmd == "flavors":
						show_flavors()
					elif cmd == "all":
						show_all()
					else:
						usage_show()
				except:
					usage_show()
		elif issuer == "admin":
			if cmd == "can_host":
				try:
					machine_name = argv[3]
					flavor = argv[4]
					check_can_host(machine, flavor)
				except:
					usage_show()

		elif issuer == "server":
			usage_show()


if __name__ == "__main__":
    main()
