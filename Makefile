libsafe_version = 2.0-16
libsafe_dir = libsafe-$(libsafe_version)
libsafe_obj = $(libsafe_dir)/src/libsafe.so
timing_dir = timing
timing_exe = $(timing_dir)/baseline-test

build : $(libsafe_obj) thread interpose.so $(timing_exe)

$(libsafe_obj) :
	make cleanlib
	tar -xvf libsafe-$(libsafe_version).tgz
	make -C $(libsafe_dir)

thread : thread.c
	gcc -o thread thread.c -fno-builtin -lpthread

interpose.so : interpose.c
	gcc -shared -ldl -fPIC -fno-builtin interpose.c -o interpose.so

interpose.c : func_names.txt
	./gen_interpose.py

$(timing_exe) :
	make -C $(timing_dir)

.PHONY : random build clean cleanlib

random :
	./gen_interpose.py $(MAX_DELAY)
	make interpose.so

clean :
	rm -vf thread interpose.c interpose.so
	make -C $(timing_dir) clean

cleanlib :
	rm -vrf $(libsafe_dir)
