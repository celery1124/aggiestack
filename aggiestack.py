import getopt, sys

def eprint(*arg):
	print >>sys.stderr, arg

def usage():
	print "will print usage later"


def main():
	try:
		cmd = sys.argv[1]
	except:
		usage()
		sys.exit()
	try:
		opts, args = getopt.getopt(sys.argv[2:], "h", ["hardware=", "images=", "flavors="])
	except getopt.GetoptError as err:
		eprint(str(err))  # will print something like "option -a not recognized"
		usage()
		sys.exit()

	print opts
if __name__ == "__main__":
    main()
