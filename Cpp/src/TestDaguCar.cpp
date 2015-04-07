#include <iostream>
#include "robots/DaguCar.h"

int main()
{
    DaguCar car( "/dev/rfcomm1", 500 );
    car.MoveBackward( 15 );
    car.Pause( 3000 );
    car.MoveForward( 15 );
    car.Pause( 3000 );
    car.MoveLeft( 15 );
    car.Pause( 1000 );
    car.MoveRight( 15 );
    car.Pause( 1000 );
    car.MoveForwardLeft( 15 );
    car.Pause( 1000 );
    car.MoveForwardRight( 15 );
    car.Pause( 1000 );
    car.MoveBackwardLeft( 15 );
    car.Pause( 1000 );
    car.MoveBackwardRight( 15 );
    car.Pause( 1000 );
    car.Stop();
    car.Close();
}
