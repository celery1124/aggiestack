import getopt, sys

def eprint(*arg):
	print >>sys.stderr, arg

def usage_config():
	print "config usage"
	print "command arguments: config "
	print "positional arguments:"
	print "--hardware\t\tRead the hardware configuration file"
	print "--images\t\tRead the images configuration file"
	print "--flavors\t\tRead the flavor instances configuration file"

def usage_show():
	print "show usage"
	print "command arguments: "
	print "show hardware\t\tList the hardware information"
	print "show images\t\tList the images information"
	print "show flavors\t\tList the flavor information"
	print "show all\t\tList all the information"

def usage():
	usage_config()
	usage_show()

def show_hardware():
	print "show hardware later"

def show_images():
	print "show images later"

def show_flavors():
	print "show flavors later"

def show_all():
	show_hardware()
	show_images()
	show_flavors()

def do_config(option,arg):
	print option
	print arg

def main():
	try:
		cmd = sys.argv[1]
	except:
		usage()
		sys.exit()

	if(cmd == "config"):
		try:
			opts, args = getopt.getopt(sys.argv[2:], "h", ["hardware=", "images=", "flavors="])
		except getopt.GetoptError as err:
			eprint(str(err))  # will print something like "option -a not recognized"
			usage_config()
			sys.exit()
		if len(opts) == 0:
			usage_config()
		for o, a in opts:
			if o == "--hardware" or o == "images" or o == "flavors":
				do_config(o,a)
			else:
				usage_config()

	elif cmd == "show":
		try:
			cmd = sys.argv[2]
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
