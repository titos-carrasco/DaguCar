#ifndef DAGUCAR_H
#define DAGUCAR_H

#include <string>
#include <mutex>

#include "SerialPort.h"

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
        int lastCmd = -1;
        mutex lock;
        int timeout;

    public:
        DaguCar( const char *port, int timeout );
        void Close();
        void Pause( int ms );
        void Stop();
        void MoveForward( int speed );
        void MoveBackward( int speed );
        void MoveLeft( int speed );
        void MoveRight( int speed );
        void MoveForwardLeft( int speed );
        void MoveForwardRight( int speed );
        void MoveBackwardLeft( int speed );
        void MoveBackwardRight( int speed );

    private:
        void Debug( const char *text );
        void Move( Command direction, unsigned int speed );
        void Lock();
        void Unlock();
};

#endif // DAGUCAR_H
