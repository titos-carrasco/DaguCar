#include "DaguCar.h"

/** \brief Constructor for an object to control the DaguCar/iRacer car
 *
 * \param port string: Bluetooth port connected to the car. Something like "/dev/rfcomm0" in Linux or "COM3:" in Windows
 *
 */
DaguCar::DaguCar(string port)
{
    for(int i=0; i<4; i++)
    {
        int err = ser.Open(port.c_str(), 9600);
        if(err==1)
        {
            isConnected = true;
            Debug("DaguCar: Conectado a 9600bps");
            return;
        }
    }
    Debug("DaguCar: No se pudo conectar a la puerta especificada");
}

/** \brief Exclusive access to the car
 *
 * \return bool: true if exclusive access is granted
 *
 */
bool DaguCar::Lock()
{
    lock.lock();
    if(isConnected)
    {
        return true;
    }
    else
    {
        lock.unlock();
        return false;
    }
}

/** \brief Release exclusive access to the car
 *
 * \return void
 *
 */
void DaguCar::Unlock()
{
    lock.unlock();
}

/** \brief Simple internal method to show messages
 *
 * \param text string: Text to show in standard error
 * \return void
 *
 */
void DaguCar::Debug(string text)
{
    cerr << text << endl;
}

/** \brief To detect if I have a connection to the car
 *
 * \return bool: true if I have a connection
 *
 */
bool DaguCar::IsConnected()
{
    return isConnected;
}

/** \brief Close the connection to the car
 *
 * \return void
 *
 */
void DaguCar::Close()
{
    if(Lock())
    {
        ser.Close();
        isConnected = false;
        Unlock();
    }
}

/** \brief Move the car
 *
 * \param direction Command: Type of move for the car
 * \param speed unsigned int: speed for the car (0 - 15)
 * \return void
 *
 */
void DaguCar::Move(Command direction, unsigned int speed)
{
    if(Lock())
    {
        int dir = direction << 4;
        speed = speed & 0x0F;
        int cmd = dir | speed;
        if(cmd!=lastCmd)
        {
            ser.WriteChar(cmd);
            lastCmd=cmd;
        }
        Unlock();
    }
}

/** \brief Stop the car
 *
 * \return void
 *
 */
void DaguCar::Stop()
{
    Move(DaguCar::CMD_STOP, 0);
}
