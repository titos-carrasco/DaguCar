#ifndef DAGUCAR_H
#define DAGUCAR_H

#include "../utils/Lock.h"
#include "../utils/SerialPort.h"

using namespace std;

class DaguCar
{
    private:
        enum Command
        {
            CMD_STOP = 0,
            CMD_FORWARD = 1,
            CMD_BACKWARD = 2,
            CMD_LEFT = 3,
            CMD_RIGHT = 4,
            CMD_FORWARD_LEFT = 5,
            CMD_FORWARD_RIGHT = 6,
            CMD_BACKWARD_LEFT = 7,
            CMD_BACKWARD_RIGHT = 8
        };
        SerialPort *ser;
        Lock lock;
        int lastCmd;
        int timeout;

    public:
        DaguCar( const char *port, unsigned int timeout );
        void Close();
        void Pause( unsigned int ms );
        void Stop();
        void MoveForward( unsigned int speed );
        void MoveBackward( unsigned int speed );
        void MoveLeft( unsigned int speed );
        void MoveRight( unsigned int speed );
        void MoveForwardLeft( unsigned int speed );
        void MoveForwardRight( unsigned int speed );
        void MoveBackwardLeft( unsigned int speed );
        void MoveBackwardRight( unsigned int speed );

    private:
        void Debug( const char *text );
        void Move( Command direction, unsigned int speed );
};

#endif // DAGUCAR_H
