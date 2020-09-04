#include <fcntl.h>
#include <stdio.h>
#include <errno.h>
#include <getopt.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/types.h>
#include <linux/input.h>
#include <linux/hidraw.h>
#include <netdb.h>


#define KNXHIDPACKETLEN	56
#define HIDRAWNAMELEN 20
#define PORT    5555
#define MAXMSG  512


int open_knx_cemi(char *hidraw);
int read_from_knx_cemi(int fd, unsigned char *packet);
int write_to_knx_cemi(int fd, unsigned char *packet);
int close_knx_cemi(int fd);
int make_socket(uint16_t port);
void init_sockaddr (struct sockaddr_in *name,
		const char *hostname,
		uint16_t port);
int read_from_client(int filedes, unsigned char *packet);
int write_to_client(int filedes, unsigned char *packet, int len);

int open_knx_cemi(char *hidraw) {
	struct hidraw_devinfo info;
	int res;
	int fd;

	fd = open(hidraw, O_RDWR);
	if (fd < 0) {
		perror("open");
		exit(EXIT_FAILURE);
	}

	return fd;
}

int read_from_knx_cemi(int fd, unsigned char *packet) {
	int res;
	int i;

	res = read(fd, packet, KNXHIDPACKETLEN);
	if (res < 0) {
		perror("read");
		exit(EXIT_FAILURE);
	}
	else {
		for (i = 0; i < res; i++) printf("%02x", packet[i]);
	}
	puts("");

	return res;
}

int write_to_knx_cemi(int fd, unsigned char *packet) {
	int res;

	res = write(fd, packet, KNXHIDPACKETLEN);
	if (res < 0) {
		perror("write");
		exit(EXIT_FAILURE);
	}

	return res;
}

int close_knx_cemi(int fd) {
	int res;

	res = close(fd);
	if (res < 0) {
		perror("close");
		exit(EXIT_FAILURE);
	}

	return res;
}

int make_socket(uint16_t port) {
    int sock;
    struct sockaddr_in name;

    sock = socket (PF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
    	perror("socket");
    	exit(EXIT_FAILURE);
    }
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int)) < 0) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    name.sin_family = AF_INET;
    name.sin_port = htons(port);
    name.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind (sock, (struct sockaddr *)&name, sizeof(name)) < 0) {
    	perror ("bind");
    	exit(EXIT_FAILURE);
    }

    return sock;
}

void init_sockaddr (struct sockaddr_in *name,
		const char *hostname,
		uint16_t port) {
	struct hostent *hostinfo;

	name->sin_family = AF_INET;
	name->sin_port = htons (port);
	hostinfo = gethostbyname (hostname);

	if (hostinfo == NULL) {
		fprintf (stderr, "Unknown host %s.\n", hostname);
		exit(EXIT_FAILURE);
	}
	name->sin_addr = *(struct in_addr *)hostinfo->h_addr;
}

int read_from_client(int filedes, unsigned char *packet) {
	int nbytes, i;
	char buffer[KNXHIDPACKETLEN * 2 + 1];

	nbytes = read(filedes, buffer, KNXHIDPACKETLEN * 2 + 1);
	if (nbytes < 0) {
		perror("read");
		return -1;
	} else if (nbytes == 0)
		return -1;
	else {
		if (buffer[nbytes - 1] == '\n' || buffer[nbytes - 1] == '\r')
			nbytes--;
		if (buffer[nbytes - 1] == '\n' || buffer[nbytes - 1] == '\r')
			nbytes--;
		if ((nbytes % 2) != 0) {
			//write(filedes, "Odd length string\n", 19);
			return 0;
		}
		for (i = 0; i < nbytes / 2; i++) {
			if (sscanf(&buffer[i * 2], "%2hhx", &packet[i]) != 1) {
				//write(filedes, "Non hex char found\n", 20);
				return 0;
			}
		}
		fprintf(stderr, "Server: got message %s len %d\n", buffer, nbytes);
		return i;
	}
}

int write_to_client(int filedes, unsigned char *packet, int len) {
	char buffer[KNXHIDPACKETLEN * 2 + 1];
	int i;

	for (i = 0; i < len; i++) {
		sprintf(&buffer[i * 2], "%02x", packet[i]);
	}
	buffer[len * 2] = '\n';
	write(filedes, buffer, len * 2 + 1);
}

// http://www.gnu.org/software/libc/manual/html_node/Server-Example.html
int main(int argc, char *argv[]) {
	fd_set active_fd_set, read_fd_set;
	struct sockaddr_in clientname;
	static char *shortopts = "hdpi";
	static struct option longopts[] = { { "help", 0, NULL, 'h' }, { "host", 1,
			NULL, 's' }, { "port", 1, NULL, 'p' },
			{ "dev-hidraw", 1, NULL, 'd' }, { 0, 0, 0, 0 }, };
	char *dev_hidraw = "/dev/hidraw1";
	char *port = "8765";
	char *host = "172.20.35.81";
	char *packet;
	size_t size;
	int option_index = 0;
	int fd_cemi;
	int sock;
	int c;
	int i;
	int client_fds[64];

	while ((c = getopt_long(argc, argv, shortopts, longopts, &option_index))
			!= -1) {
		switch (c) {
		case 'h': {
			printf("Usage: daemon [OPTION]...\n");
			printf(
					"-d, --dev-hidraw\t\t\tThe hidraw device (as /dev/hidraw2) \n");
			exit(0);
		}
		case 'd': {
			dev_hidraw = optarg;
			break;
		}
		case 'p': {
			port = optarg;
			break;
		}
		case 'i': {
			host = optarg;
			break;
		}
		}
	}

	sock = make_socket((uint16_t) PORT);
	if (listen(sock, 1) < 0) {
		perror("listen");
		exit(EXIT_FAILURE);
	}

	fd_cemi = open_knx_cemi(dev_hidraw);
	packet = (char *) malloc(KNXHIDPACKETLEN);

	FD_ZERO(&active_fd_set);
	FD_SET(sock, &active_fd_set);
	FD_SET(fd_cemi, &active_fd_set);
	int j;
	for (j = 0; j < 64; j++) {
		client_fds[j] = -1;
	}

	while (1) {
		read_fd_set = active_fd_set;
		if (select(FD_SETSIZE, &read_fd_set, NULL, NULL, NULL) < 0) {
			perror("select");
			exit(EXIT_FAILURE);
		}

		for (i = 0; i < FD_SETSIZE; ++i)
			if (FD_ISSET(i, &read_fd_set)) {
				if (i == sock) {
					int new_client;
					socklen_t len;
					len = sizeof(clientname);
					new_client = accept(sock, (struct sockaddr *) &clientname,
							&len);
					if (new_client < 0) {
						perror("accept");
						exit(EXIT_FAILURE);
					}
					fprintf(stderr, "Server: connect from host %d, port %hd.\n",
							inet_ntoa(clientname.sin_addr),
							ntohs(clientname.sin_port));
					FD_SET(new_client, &active_fd_set);
					for (j = 0; j < 64; j++) {
						if (client_fds[j] == -1) {
							client_fds[j] = new_client;
							break;
						}
					}
				} else if (i == fd_cemi) {
					int l = read_from_knx_cemi(fd_cemi, packet);
					for (j = 0; j < 64; j++) {
						if (client_fds[j] > 0) {
							write_to_client(client_fds[j], packet, l);
						}
					}
				} else {
					if (read_from_client(i, packet) >= 0) {
						write_to_knx_cemi(fd_cemi, packet);
					} else {
						FD_CLR(i, &active_fd_set);
						for (j = 0; j < 64; j++) {
							if (client_fds[j] == i) {
								client_fds[j] = -1;
								break;
							}
						}
						close(i);
					}

				}
			}
	}

	return 0;
}
