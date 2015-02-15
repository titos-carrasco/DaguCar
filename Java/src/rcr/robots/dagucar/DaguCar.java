package rcr.robots.dagucar;

import java.io.IOException;

public class DaguCar {
    // Comandos para el auto
    public static final int CMD_STOP = 0;
    public static final int CMD_FORWARD = 1;
    public static final int CMD_BACKWARD = 2;
    public static final int CMD_LEFT = 3;
    public static final int CMD_RIGHT = 4;
    public static final int CMD_LEFT_FORWARD = 5;
    public static final int CMD_RIGHT_FORWARD = 6;
    public static final int CMD_LEFT_BACKWARD = 7;
    public static final int CMD_RIGHT_BACKWARD = 8;

    private Serial serial;
    private int lastCmd = -1;

    public DaguCar( String portName, int bauds, int timeout ) throws IOException {
        for(int i=1; i<=10; i++ ) {
            try {
                serial = new Serial( portName, bauds, timeout );
                try {
                    // lee residuos dejados en la última conexión
                    serial.Read1UByte();
                } catch ( IOException e ) {
                }
                return;
            } catch( Exception e ){
            }
        }
        throw new IOException();
    }

    public void Close() {
        serial.Close();
    }

    public void Wait( int ms ) {
        try {
            Thread.sleep(ms);
        } catch(InterruptedException ex) {
            Thread.currentThread().interrupt();
        }
    }

    public void Move( int direction, int speed ) throws IOException {
        if(direction < CMD_STOP || direction > CMD_RIGHT_BACKWARD ) direction =CMD_STOP;
        speed = speed | 0x000F;

        int cmd = (direction<<4) | speed;
        if( cmd!=lastCmd ) {
            byte[] packet = new byte[] { (byte)cmd };
            serial.Write(packet);
            lastCmd = cmd;
        }
    }

    public void Stop() throws IOException {
        Move( CMD_STOP, 0 );
    }
}
