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
		self.hw_list = []
	def insert(self,hw_inst):
		hw_dict = OrderedDict();
		hw_dict["name"] = hw_inst[0];
		hw_dict["ip"] = hw_inst[1];
		hw_dict["mem"] = hw_inst[2];
		hw_dict["num-disk"] = hw_inst[3];
		hw_dict["num-vcpus"] = hw_inst[4];
		self.hw_list.append(hw_dict)
	def show(self):
		try:
			t = PrettyTable(self.hw_list[0].keys())
		except:
			print "No hardware information yet"
		for i in self.hw_list:
			t.add_row(i.values())
		print t

class Images:
	def __init__(self):
		self.img_list = []
	def insert(self,img_inst):
		img_dict = OrderedDict() 
		img_dict["image-name"] = img_inst[0]
		img_dict["path"] = img_inst[1]
		self.img_list.append(img_dict)
	def show(self):
		try:
			t = PrettyTable(self.img_list[0].keys())
		except:
			print "No hardware information yet"
		for i in self.img_list:
			t.add_row(i.values())
		print t

class Flavors:
	def __init__(self):
		self.flv_list = []
	def insert(self,flv_inst):
		flv_dict = OrderedDict() 
		flv_dict["type"] = flv_inst[0]
		flv_dict["mem"] = flv_inst[1]
		flv_dict["num-disk"] = flv_inst[2]
		flv_dict["num-vcpus"] = flv_inst[3]
		self.flv_list.append(flv_dict)
	def show(self):
		try:
			t = PrettyTable(self.flv_list[0].keys())
		except:
			print "No hardware information yet"
		for i in self.flv_list:
			t.add_row(i.values())
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

HW=Hardware()
IMG=Images()
FLV=Flavors()

def main():
	while True:
		argv = raw_input('> ')
		argv = argv.split();
		try:
			program_name = argv[0]
			cmd = argv[1]
		except:
			usage()
			sys.exit()
		# valid test
		if program_name != "aggiestack":
			usage()
			sys.exit()

		if(cmd == "config"):
			try:
				opts, args = getopt.getopt(argv[2:], "h", ["hardware=", "images=", "flavors="])
			except getopt.GetoptError as err:
				eprint(str(err))  # will print something like "option -a not recognized"
				usage_config()
				sys.exit()
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
				sys.exit()

	
if __name__ == "__main__":
    main()
