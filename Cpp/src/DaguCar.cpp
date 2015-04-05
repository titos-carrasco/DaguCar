#include <iostream>
#include <time.h>
#include "DaguCar.h"

DaguCar::DaguCar( const char *port, int _timeout )
{
    timeout = _timeout;
    for(int i=0; i<10 ; i++)
    {
        ser = new SerialPort( port, 9600 );
        Pause( 1000 );
        return;
    }
    throw -1;
}

void DaguCar::Close()
{
    Lock();
    ser->Close();
    Unlock();
}

void DaguCar::Pause( int ms )
{
    clock_t time_end;
    time_end = clock() + ms * CLOCKS_PER_SEC/1000;
    while (clock() < time_end)
    {
    }
}


void DaguCar::Stop()
{
    Move( DaguCar::CMD_STOP, 0 );
}

void DaguCar::MoveForward( int speed )
{
    Move( DaguCar::CMD_FORWARD, speed & 0x0F );
}

void DaguCar::MoveBackward( int speed )
{
    Move( DaguCar::CMD_BACKWARD, speed & 0x0F );
}

void DaguCar::MoveLeft( int speed )
{
    Move( DaguCar::CMD_LEFT, speed & 0x0F );
}

void DaguCar::MoveRight( int speed )
{
    Move( DaguCar::CMD_RIGHT, speed & 0x0F );
}

void DaguCar::MoveForwardLeft( int speed )
{
    Move( DaguCar::CMD_FORWARD_LEFT, speed & 0x0F );
}

void DaguCar::MoveForwardRight( int speed )
{
    Move( DaguCar::CMD_FORWARD_RIGHT, speed & 0x0F );
}

void DaguCar::MoveBackwardLeft( int speed )
{
    Move( DaguCar::CMD_BACKWARD_LEFT, speed & 0x0F );
}

void DaguCar::MoveBackwardRight( int speed )
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
    Unlock();
}

void DaguCar::Lock()
{
    lock.lock();
}

void DaguCar::Unlock() {
    lock.unlock();
}
