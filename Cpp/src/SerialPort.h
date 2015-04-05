#ifndef SERIAL_H
#define SERIAL_H

#include <strings.h>
#include <termios.h>
#include <fcntl.h>
#include <unistd.h>

class SerialPort
{
    public:
        SerialPort( const char *port, int bauds );
        ~SerialPort();
        void Close();
        int Write( unsigned char byte );

    private:
        int fd;
};

#endif // SERIAL_H
