#include <iostream>
#include "DaguCar.h"

int main()
{
    DaguCar car("/dev/rfcomm1");
    if(car.IsConnected())
    {
        car.Move(DaguCar::CMD_FORWARD, 15);
        sleep(1);
        car.Move(DaguCar::CMD_LEFT_FORWARD, 15);
        sleep(1);
        car.Move(DaguCar::CMD_RIGHT_FORWARD, 15);
        sleep(1);
        car.Move(DaguCar::CMD_BACKWARD, 15);
        sleep(1);
        car.Move(DaguCar::CMD_LEFT_BACKWARD, 15);
        sleep(1);
        car.Move(DaguCar::CMD_RIGHT_BACKWARD, 15);
        sleep(1);
        car.Move(DaguCar::CMD_LEFT, 15);
        sleep(1);
        car.Move(DaguCar::CMD_RIGHT, 15);
        sleep(1);
        car.Stop();
        car.Close();
    }
    return 0;
}
