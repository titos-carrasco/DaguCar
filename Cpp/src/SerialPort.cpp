#include "SerialPort.h"

SerialPort::SerialPort( const char *port, int bauds )
{
    // O_NOCTTY=no controlling terminal, O_NDELAY=dont use DCD
    fd = open( port, O_RDWR | O_NOCTTY | O_NDELAY );
    if(fd == -1)
        throw -1;

    // FNDELAY=non blocking read, return 0
    fcntl( fd, F_SETFL, FNDELAY );

    // limpia estructura termios
    struct termios options;
    tcgetattr( fd, &options );
    bzero( &options, sizeof( options ) );

    // la velocidad
    speed_t speed;
    switch(bauds)
    {
        case 110    : speed = B110; break;
        case 300    : speed = B300; break;
        case 600    : speed = B600; break;
        case 1200   : speed = B1200; break;
        case 2400   : speed = B2400; break;
        case 4800   : speed = B4800; break;
        case 9600   : speed = B9600; break;
        case 19200  : speed = B19200; break;
        case 38400  : speed = B38400; break;
        case 57600  : speed = B57600; break;
        case 115200 : speed = B115200; break;
        default     : throw -2;
    }
    cfsetispeed(&options, speed);
    cfsetospeed(&options, speed);

    // not owner
    options.c_cflag |= ( CLOCAL | CREAD );

    // 8N1
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;

    // raw input
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);

    // ignore parity and break
    options.c_iflag |= ( IGNPAR | IGNBRK );

    // raw output
    options.c_oflag &= ~OPOST;

    // no wait
    options.c_cc[VTIME]=0;
    options.c_cc[VMIN]=0;

    // los cambios toman efecto desde ahora
    tcsetattr(fd, TCSANOW, &options);
}

SerialPort::~SerialPort()
{
    Close();
}

void SerialPort::Close()
{
    close( fd );
}

int SerialPort::Write( unsigned char byte )
{
    int n = write( fd, &byte, 1);
    return n;
}
