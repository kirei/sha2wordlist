PROG=		sha2wordlist
SRCS=		sha2wordlist.c sha2.c
OBJS=		sha2wordlist.o sha2.o
LDFLAGS=
LIBS=

IDENT_OPTS=	-v -nip

all: $(PROG)

$(PROG): $(OBJS)
	gcc -o $@ $(LDFLAGS) $(OBJS) $(LIBS)

clean::
	rm -f $(PROG) $(OBJS)

indent::
	indent $(INDENT_OPTS) < sha2wordlist.c

sha2wordlist.deb: $(PROG)
	sh deb.sh

container-build-deb:
	docker build -t sha2wordlist .
	docker create --name sha2wordlist sha2wordlist
	docker cp sha2wordlist:/src/sha2wordlist.deb .
	docker rm -f sha2wordlist
	docker rmi -f sha2wordlist
