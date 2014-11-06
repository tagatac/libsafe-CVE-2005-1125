#!/usr/bin/env python

import sys, random
if len(sys.argv) > 1: MAXDELAY = int(sys.argv[1])
else: MAXDELAY = 50

# interpose.c template strings
header = ""
libraries = "#define _GNU_SOURCE\n" \
            "#include <dlfcn.h>\n"  \
            "#include <time.h>\n"   \
            "#include <wchar.h>\n"  \
            "#include <signal.h>\n" \
            "#include <unistd.h>\n" \
            "#include <setjmp.h>\n" \
            "#include <sys/time.h>\n" \
            "#include <sys/stat.h>\n" \
            "#include <stdio.h>\n\n"
func_head = "{ret}{space}{func_name}({func_args})\n"
# add "{\n"
func_body1 = "\tstatic {ret} (*real_{func_name})({func_args_no_id}) = NULL;\n\tint i;\n" #\
func_timespec1 = "\tstruct timespec req = {(time_t) 0, (long) "
func_timespec2 = "{delay}"
func_timespec3 ="};\n\tnanosleep(&req, NULL);\n"
func_timespec ="\tfor(i=0; i<{delay}; i++)\n\t\tasm(\"nop;\");\n"
func_body2 = "\tif(!real_{func_name})\n"
func_body3 = "\t\treal_{func_name} = dlsym(RTLD_NEXT, \"{func_name}\");\n"
func_ret = "\treturn real_{func_name}({func_args_id});\n" \
# add"}"

last_lib = ""
interpose_file = header + libraries
# Set of specific functions to add in
extra = '''void qsort(void * base, size_t nmemb, size_t size, int (*compar)(const void * , const void * ))
{
	static void (*real_qsort)(void *, size_t, size_t, int (*compar)(const void *, const void *)) = NULL;
	int i;
	for(i=0; i<''' + str(random.randint(0, MAXDELAY)) + '''; i++)
		asm("nop;");
	if(!real_qsort)
		real_qsort = dlsym(RTLD_NEXT, "qsort");
	return real_qsort(base, nmemb, size, compar);
}'''
extra += '''void __libc_start_main(int (*main) (int, char * *, char * *), int argc, char * * ubp_av, void (*init) (void), void (*fini) (void), void (*rtld_fini) (void), void (* stack_end))
{
	static void (*real___libc_start_main)(int (*main) (int, char * *, char * *), int , char * * , void (*init) (void), void (*fini) (void), void (*rtld_fini) (void), void (* stack_end)) = NULL;
	int i;
	for(i=0; i<''' + str(random.randint(0, MAXDELAY)) + '''; i++)
		asm("nop;");
	if(!real___libc_start_main)
		real___libc_start_main = dlsym(RTLD_NEXT, "__libc_start_main");
	return real___libc_start_main(main, argc, ubp_av, init, fini, rtld_fini, stack_end);
}'''

# Functions to exclude
exclude = {"strcpy": True,
	   "strcat": True,
	   "getwd": True,
	   "gets": True,
	   "scanf": True,
	   "realpath": True,
	   "sprintf": True}

# splits types and ids into seperate lists, returns a tuple of 2 lists
# list 1 is of types, list 2 is of ids
# 'restrict' keyword is filtered out, and "..." is filtered out
def split_func_args(func_args):
	ret_args = ([],[])
	args = func_args.split(',')
	for arg in args:
		arg = arg.strip()
		if (arg.rfind("*") >= 0): # If parameter is of type pointer
			star = arg.rfind("*")+1
			arg_type = arg[0:star]
			id = arg[star:len(arg)].replace("restrict", " ").strip()
			ret_args[0].append(arg_type)
			ret_args[1].append(id)
		elif(arg.rfind(" ") >= 0):
			space = arg.rfind(" ")
			arg_type = arg[0:space]
			id = arg[space:len(arg)].replace("restrict", " ").strip()
			ret_args[0].append(arg_type)
			ret_args[1].append(id)
		elif(arg == "void"):
			ret_args[0].append(arg)
			ret_args[1].append("")
		elif(arg.find("...")): # for variable arguments
			print(arg)
	return ret_args

# takes in a list of function argument types
def get_func_args_no_id(func_args_type):
	return ", ".join(func_args_type)

# takes in a list of function arguments
def get_func_args(func_args):
	new_func_list = []
	for i in range(0,len(func_args[0])):
		new_func_list.append(func_args[0][i] + " " + func_args[1][i])
	return ", ".join(new_func_list)

# takes in a list of function argument id
def get_func_args_id(func_args_id):
	return ", ".join(func_args_id)

with open("func_names.txt") as file:
	for line in file:
		line = line.strip()
		if line is "":
			continue

		# Libraries have # in front
		elif line[0] is "#":
			continue

		# If no # in front and ends with ;, then assume it is a function
		elif line[len(line)-1] is ";":
			if line.count(';') > 1:
				print("Error(3): " + line)
				continue

			if line.count('.') == 3:
				# Future work: manage variable length arguments
				continue

			# func_decl[0] is everything before '(''
			func_decl = line.split('(', 1)
			pre_paren = func_decl[0]
			func_args_str = func_decl[1][0:len(func_decl[1])-2] # strip away ");"
			if (pre_paren.rfind("*") >=0): # If return type is of pointer
				star = pre_paren.rfind("*")+1
				ret_type = pre_paren[0:star]
				func_name = pre_paren[star:len(pre_paren)].strip()
#				if exclude.get(func_name, False):
#					print("Excluding: " + func_name)
#					continue
				func_args = split_func_args(func_args_str)

				# Create function using template strings
				function = func_head.format(ret=ret_type,space="",
					func_name=func_name, func_args=get_func_args(func_args)) + "{\n"
				function += func_body1.format(ret=ret_type,
					func_name=func_name, func_args_no_id=get_func_args_no_id(func_args[0]))
				#function += func_timespec1
				function += func_timespec.format(delay=random.randint(0, MAXDELAY))
				#function += func_timespec3
				function += func_body2.format(func_name=func_name)
				function += func_body3.format(func_name=func_name)
				function += func_ret.format(func_name=func_name,
					func_args_id=get_func_args_id(func_args[1])) + "}\n"
#				if (func_name == "fprintf_s"):
#					print(function)
#					print(":" + func_args)
				interpose_file += function + "\n"

			elif (pre_paren.rfind(" ") >= 0):
				space = pre_paren.rfind(" ")
				ret_type = pre_paren[0:space]
				func_name = pre_paren[space:len(pre_paren)].strip()
#				if exclude.get(func_name, False):
#					print("Excluding: " + func_name)
#					continue
				func_args = split_func_args(func_args_str)

				# Create function using template strings
				function = func_head.format(ret=ret_type,space=" ",
					func_name=func_name, func_args=get_func_args(func_args)) + "{\n"
				function = function + func_body1.format(ret=ret_type,
					func_name=func_name, func_args_no_id=get_func_args_no_id(func_args[0]))
				#function += func_timespec1
				function += func_timespec.format(delay=random.randint(0, MAXDELAY))
				#function += func_timespec3
				function += func_body2.format(func_name=func_name)
				function += func_body3.format(func_name=func_name)
				function += func_ret.format(func_name=func_name,
					func_args_id=get_func_args_id(func_args[1])) + "}\n"
			#	if (func_name == "fprintf_s"):
			#		print(function)
			#		print(func_args)
				interpose_file += function + "\n"

			else:
				print("Error(2): " + pre_paren)
				continue
		else:
			print("Error(1): " + line)
			continue

with open("interpose.c", "w") as outfile:
	interpose_file
	outfile.write(interpose_file)
