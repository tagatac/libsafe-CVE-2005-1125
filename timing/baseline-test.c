#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>

int main(int argc, char **argv)
{
	if (argc > 2)
	{
		fprintf(stderr, "Usage: ./baseline-test <times to run>");
		exit(1);
	}
	char buf[33];
	char str[] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
	int i, j;
	double total_time;
	j = 10000000;
	if (argc > 1)
		j = atoi(argv[1]);

	struct timeval start, end;
	gettimeofday(&start, 0);

	for (i=0;i<j;i++)
	{
		strcpy(buf, str);
		str[31] += 1;
	}

	gettimeofday(&end, 0);
	total_time = 1e6 * (end.tv_sec-start.tv_sec) + (end.tv_usec-start.tv_usec);
	printf("Average time of %d to run strncpy: %f microseconds\n", j, total_time/j);
	return 0;
}
