#ifndef DAGUCAR_H
#define DAGUCAR_H

#include <string>
#include <mutex>

#include "serialib/serialib.h"

using namespace std;


/** \brief Class to control the DaguCar/iRacer car
 */
class DaguCar
{
    public:
        /** \brief Commands to move the DaguCar/iRacer car
         */
        enum Command {
            CMD_STOP = 0,
            CMD_FORWARD = 1,
            CMD_BACKWARD = 2,
            CMD_LEFT = 3,
            CMD_RIGHT = 4,
            CMD_LEFT_FORWARD = 5,
            CMD_RIGHT_FORWARD = 6,
            CMD_LEFT_BACKWARD = 7,
            CMD_RIGHT_BACKWARD = 8
        };

    private:
        mutex lock;
        serialib ser;
        int lastCmd = 0;
        bool isConnected = false;

    public:
        DaguCar(string port);
        bool IsConnected();
        void Close();
        void Move(Command direction, unsigned int speed);
        void Stop();

    private:
        bool Lock();
        void Unlock();
        void Debug(string text);
};

#endif // DAGUCAR_H
