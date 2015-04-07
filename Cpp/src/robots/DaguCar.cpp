#include <iostream>
#include <time.h>
#include <unistd.h>

#include "DaguCar.h"

DaguCar::DaguCar( const char *port, unsigned int _timeout )
{
    timeout = _timeout;
    lastCmd = -1;
    for(int i=0; i<10 ; i++)
    {
        ser = new SerialPort( port, 9600, timeout );
        Pause( 1000 );
        return;
    }
    throw -1;
}

void DaguCar::Close()
{
    lock.lock();
    ser->Close();
    lock.unlock();
}

void DaguCar::Pause( unsigned int ms )
{
    usleep( ms * 1000 );
}


void DaguCar::Stop()
{
    Move( DaguCar::CMD_STOP, 0 );
}

void DaguCar::MoveForward( unsigned int speed )
{
    Move( DaguCar::CMD_FORWARD, speed & 0x0F );
}

void DaguCar::MoveBackward( unsigned int speed )
{
    Move( DaguCar::CMD_BACKWARD, speed & 0x0F );
}

void DaguCar::MoveLeft( unsigned int speed )
{
    Move( DaguCar::CMD_LEFT, speed & 0x0F );
}

void DaguCar::MoveRight( unsigned int speed )
{
    Move( DaguCar::CMD_RIGHT, speed & 0x0F );
}

void DaguCar::MoveForwardLeft( unsigned int speed )
{
    Move( DaguCar::CMD_FORWARD_LEFT, speed & 0x0F );
}

void DaguCar::MoveForwardRight( unsigned int speed )
{
    Move( DaguCar::CMD_FORWARD_RIGHT, speed & 0x0F );
}

void DaguCar::MoveBackwardLeft( unsigned int speed )
{
    Move( DaguCar::CMD_BACKWARD_LEFT, speed & 0x0F );
}

void DaguCar::MoveBackwardRight( unsigned int speed )
{
    Move( DaguCar::CMD_BACKWARD_RIGHT, speed & 0x0F );
}

void DaguCar::Debug( const char *text )
{
    cerr << text << endl;
}

void DaguCar::Move( Command direction, unsigned int speed )
{
    lock.lock();
    int dir = direction << 4;
    speed = speed & 0x0F;
    int cmd = dir | speed;
    if( cmd!=lastCmd ) {
        ser->Write( cmd );
        lastCmd=cmd;
    }
    lock.unlock();
}

