package rcr.robots.dagucar;

import java.io.IOException;

class Main {
    public static void main( String [] args ) {
        try {
            DaguCar car = new DaguCar( args[0], 9600, 1000);
            System.out.println("Conectado a la puerta serial");

            car.Move( car.CMD_FORWARD, 15 );
            car.Wait(3000);
            car.Move( car.CMD_BACKWARD, 15 );
            car.Wait(3000);
            car.Stop();
            car.Close();
        } catch ( Exception e ) {
            System.out.println( "Exception recibida: " + e.toString());
        }

    }
}
