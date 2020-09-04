TARGET=knxstack-usbhid-daemon
SOURCE=usbhid.c

all: $(TARGET)

clean: 
	rm -f knxstack-usbhid-daemon

$(TARGET) : $(SOURCE)
	$(CC) -o $@ $<
