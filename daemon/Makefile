TARGET=knxstack-cemi-daemon
SOURCE=linux_cemi.c

all: $(TARGET)

clean: 
	rm -f knxstack-cemi-daemon

$(TARGET) : $(SOURCE)
	$(CC) -o $@ $<
