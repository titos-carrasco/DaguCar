package rcr.robots.dagucar;

import gnu.io.NoSuchPortException;
import gnu.io.PortInUseException;
import gnu.io.UnsupportedCommOperationException;

import java.io.IOException;

import rcr.utils.Serial;
import rcr.utils.SerialTimeoutException;

/**
 * Clase para interactuar con el rauto Dagucar/iRacer
 * Mayor información en https://www.sparkfun.com/products/11162.
 * En Chile lo comercializaba Olimex
 *
 * @author Roberto Carrasco
 */
 public class DaguCar {
    /** Detiene el auto */
    private static final int CMD_STOP = 0;
    /**  Mueve el auto hacia adelante */
    private static final int CMD_FORWARD = 1;
    /**  Mueve el auto hacia atrás */
    private static final int CMD_BACKWARD = 2;
    /**  Mueve las ruedas del auto hacia la izquierda */
    private static final int CMD_LEFT = 3;
    /**  Mueve las ruedas del auto hacia la derecha */
    private static final int CMD_RIGHT = 4;
    /**  Mueve el auto hacia adelante e izquierda */
    private static final int CMD_FORWARD_LEFT = 5;
    /**  Mueve el auto hacia adelante y derecha */
    private static final int CMD_FORWARD_RIGHT = 6;
    /**  Mueve el auto hacia atrás e izquierda */
    private static final int CMD_BACKWARD_LEFT = 7;
    /**  Mueve el auto hacia atrás y derecha */
    private static final int CMD_BACKWARD_RIGHT = 8;

    /** el objeto de la conexión serial */
    private Serial serial;
    /** el último comando ejecutado para evitar enviarlo dos veces */
    private int lastCmd = -1;

    /**
     * Construye el objeto para manipular el auto DaguCar/iRacer a través de la puerta serial
     *
     * @param port la puerta serial a la cual conectarse ("/dev/rfcomm1", "COM1")
     * @param timeout tiempo de espera en ms para recibir los datos desde el S2
     * @throws NoSuchPortException
     * @throws PortInUseException
     * @throws UnsupportedCommOperationException
     * @throws IOException
    */
    public DaguCar( String port, int timeout ) throws NoSuchPortException, PortInUseException, UnsupportedCommOperationException, IOException {
        for( int i = 1; ; i++ ) {
            try {
                serial = new Serial( port, 9600, timeout );
                Pause( 1000 );
                serial.FlushRead( 2000 );
                return;
            } catch( Exception e ){
                if( i > 10 ) {
                    throw e;
                }
            }
        }
    }

    /***
     * Cierra la conexión con el auto
     */
    public synchronized void Close() {
        serial.Close();
    }

    /**
     * Suspende la ejecución del thread por un número dado de milisegundos
     *
     * @param ms el número de ms a suspender el thread
     */
    public void Pause( int ms ) {
        serial.Pause( ms );
    }

    /*
     * Comandos para el auto
     */

    /***
     * Detiene el auto
     *
     * @throws IOException
     */
    public synchronized void Stop() throws IOException {
        Move( CMD_STOP, 0x00 );
    }

    /***
     * Mueve el auto hacia adelante
     *
     * @throws IOException
     */
    public synchronized void MoveForward( int speed ) throws IOException {
        Move( CMD_FORWARD, speed & 0x0F );
    }

    /***
     * Mueve el auto hacia atrás
     *
     * @throws IOException
     */
    public synchronized void MoveBackward( int speed ) throws IOException {
        Move( CMD_BACKWARD, speed & 0x0F );
    }

    /***
     * Mueve las ruedas del auto hacia la izquierda
     *
     * @throws IOException
     */
    public synchronized void MoveLeft( int speed ) throws IOException {
        Move( CMD_LEFT, speed & 0x0F );
    }

    /***
     * Mueve las ruedas del auto hacia la derecha
     *
     * @throws IOException
     */
    public synchronized void MoveRight( int speed ) throws IOException {
        Move( CMD_RIGHT, speed & 0x0F );
    }

    /***
     * Mueve el auto hacia adelante e izquierda
     *
     * @throws IOException
     */
    public synchronized void MoveForwardLeft( int speed ) throws IOException {
        Move( CMD_FORWARD_LEFT, speed & 0x0F );
    }

    /***
     * Mueve el auto hacia adelante y derecha
     *
     * @throws IOException
     */
    public synchronized void MoveForwardRight( int speed ) throws IOException {
        Move( CMD_FORWARD_RIGHT, speed & 0x0F );
    }

    /***
     * Mueve el auto hacia atrás e izquierda
     *
     * @throws IOException
     */
    public synchronized void MoveBackwardLeft( int speed ) throws IOException {
        Move( CMD_BACKWARD_LEFT, speed & 0x0F );
    }

    /***
     * Mueve el auto hacia atrás y derecha
     *
     * @throws IOException
     */
    public synchronized void MoveBackwardRight( int speed ) throws IOException {
        Move( CMD_BACKWARD_RIGHT, speed & 0x0F );
    }

    /**
     * métodos privados
     */

    private void Debug( String msg ) {
        System.out.println( msg );
    }

    private void Debug( int n ) {
        System.out.println( n );
    }

    private void Move( int direction, int speed ) throws IOException {
        if( direction < CMD_STOP || direction > CMD_BACKWARD_RIGHT ) {
            direction =CMD_STOP;
        }
        speed = speed | 0x0F;

        int cmd = ( direction<<4 ) | speed;
        if( cmd != lastCmd ) {
            byte[] packet = new byte[1];
            packet[0] = (byte)cmd;
            serial.Write( packet );
            lastCmd = cmd;
        }
    }

}
