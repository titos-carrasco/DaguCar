#ifndef SERIAL_H
#define SERIAL_H

class SerialPort
{
    public:
        SerialPort( const char *port, unsigned int bauds, unsigned int timeout );
        ~SerialPort();
        void Close();
        int Write( unsigned char byte );

    private:
        int fd;
};

#endif // SERIAL_H
