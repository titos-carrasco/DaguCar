package rcr.utils;

import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;
import gnu.io.NoSuchPortException;
import gnu.io.PortInUseException;
import gnu.io.UnsupportedCommOperationException;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;
import java.util.Arrays;

import rcr.utils.SerialTimeoutException;

/**
 * Clase para realizar operaciones sobre una puerta serial
 *
 * @author Roberto Carrasco
 */
public class Serial {
    /** la puerta serial en operación */
    private SerialPort serialPort;
    /** el objeto para lecturas */
    private InputStream in;
    /** el objeto para escrituras */
    private OutputStream out;
    /** el timeout real es de 1ms */
    private int REAL_TIMEOUT = 1;
    /** el timeout del usuario */
    private int USER_TIMEOUT;
    /** el timeout del usuario lo manejamos como el número de iteraciones */
    private int TRIES;

    /**
     * Construye un nuevo objeto para interactuar con una puerta serial y abre la conexión
     *
     * @param port el nombre de la puerta ("/dev/rfcomm1", "COMM1")
     * @param bauds los bauds a operar ("2400", "9600")
     * @param timeout el timeout de cada lectura expresado en ms
     * @throws NoSuchPortException
     * @throws PortInUseException
     * @throws UnsupportedCommOperationException
     * @throws IOException
     */
    public Serial( String port, int bauds, int timeout ) throws NoSuchPortException, PortInUseException, UnsupportedCommOperationException, IOException {
        try {
            CommPortIdentifier portId = CommPortIdentifier.getPortIdentifier( port );
            serialPort = (SerialPort)portId.open( this.getClass().getName() + " " + port, timeout );
            serialPort.setSerialPortParams( bauds, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE );
            serialPort.setFlowControlMode( SerialPort.FLOWCONTROL_NONE );
            serialPort.enableReceiveTimeout( REAL_TIMEOUT );
            serialPort.enableReceiveThreshold(1);
            USER_TIMEOUT = timeout;
            TRIES = USER_TIMEOUT / REAL_TIMEOUT;
            in = serialPort.getInputStream();
            out = serialPort.getOutputStream();
        } catch ( IOException e ) {
            serialPort.close();
            throw e;
        }
    }

    /**
     * Cierra la conexión con la puerta serial
     */
    public synchronized void Close() {
        try {
            in.close();
        } catch( IOException e ) {
        }
        try {
            out.close();
        } catch( IOException e ) {
        }
        serialPort.close();
    }

    /**
     * Envía un grupo de bytes por la puerta serial
     *
     * @param bytes los bytes a enviar
     * @throws IOException
     */
    public synchronized void Write( byte[] bytes ) throws IOException {
        out.write( bytes );
        out.flush();
    }

    /**
     * Lee una línea desde la puerta serial. La lectura es realizada caracter por caracter
     *
     * @param maxLen el tamaño máximo de la línea a leer
     * @throws IOException
     * @throws SerialTimeoutException
     * @return la línea leida desde la puerta serial
     */
    public synchronized String ReadLine( int maxLen ) throws IOException, SerialTimeoutException {
        byte bytes[] = new byte[maxLen + 1];
        int pos = 0;
        int tries = 0;
        while( pos < maxLen + 1 && tries < TRIES ){
            int b = in.read();
            if( b < 0 ) {
                tries++;
                continue;
            }
            // fin de línea detectado
            if( b == 10 ){
                return new String( bytes, 0, pos );
            }
            bytes[ pos++ ] = (byte)b;
            tries = 0;
            //System.out.println(javax.xml.bind.DatatypeConverter.printHexBinary(bytes));
        }
        throw new SerialTimeoutException();
    }

    /**
     * Lee un conjunto de bytes desde la puerta serial
     *
     * @param nbytes el número de bytes a leer
     * @throws IOException
     * @throws SerialTimeoutException
     * @return los bytes leidos desde la puerta serial
     */
    public synchronized byte[] Read( int nbytes ) throws IOException, SerialTimeoutException {
        byte bytes[] = new byte[nbytes];
        //Arrays.fill( bytes, (byte)0xFF );
        int pos = 0;
        int tries = 0;
        while( pos < nbytes && tries < TRIES ){
            int b = in.read();
            if( b < 0 ) {
                tries++;
                continue;
            }
            bytes[ pos++ ] = (byte)b;
            tries = 0;
            //System.out.println(javax.xml.bind.DatatypeConverter.printHexBinary(bytes));
        }
        if( pos < nbytes ) {
            throw new SerialTimeoutException();
        }
        return bytes;
    }

    /**
     * Descarta los bytes recibidos desde la puerta serial durante un número dado de ms
     *
     * @param time los ms durante los cuales se leen bytes desde la puerta serial y se ignoran
     */
    public synchronized void FlushRead( int time ) {
        long t2, t1 = System.currentTimeMillis();
        do {
            try {
                in.read();
            } catch( Exception e ) {
            }
            t2 = System.currentTimeMillis();
        } while( (int)( t2 - t1 ) <= time );
    }

    /**
     * Lee 1 byte desde la puerta serial cmo un unsigned integer
     *
     * @throws IOException
     * @throws SerialTimeoutException
     * @return el byte leido como un unsigned integer
     */
    public int Read1UByte() throws IOException, SerialTimeoutException {
        byte[] b = Read(1);
        return b[0] & 0xFF;
    }

    /**
     * Lee 2 bytes desde la puerta serial como un unsigned integer
     *
     * @throws IOException
     * @throws SerialTimeoutException
     * @return los bytes leidos como un unsigned integer
     */
    public int Read2UBytes() throws IOException, SerialTimeoutException {
        byte[] b = Read(2);
        int n = b[0] & 0x000000FF;
        n = ( n<<8 ) | ( b[1] & 0xFF );
        return n;
    }

    /**
     * Lee 4 bytes desde la puerta serial como un unsigned long
     *
     * @throws IOException
     * @throws SerialTimeoutException
     * @return los bytes leidos como un unsigned long
     */
    public long Read4UBytes() throws IOException, SerialTimeoutException {
        byte[] b = Read(4);
        long n = b[0] & 0x000000FF;
        n = ( n << 8 ) | ( b[1] & 0xFF );
        n = ( n << 8 ) | ( b[2] & 0xFF );
        n = ( n << 8 ) | ( b[3] & 0xFF );
        return n;
    }

    /**
     * Lee 4 bytes desde la puerta serial como un signed long
     *
     * @throws IOException
     * @throws SerialTimeoutException
     * @return los bytes leidos como un unsigned long
     */
    public int Read4Bytes() throws IOException, SerialTimeoutException {
        long n = Read4UBytes();
        return (int) n;
    }

    /**
     * Suspende la ejecución del thread un número dado de ms
     *
     * @param ms el tiempo en ms a realizar de pausa
     */
    public void Pause( int ms ) {
        try {
            Thread.sleep( ms );
        } catch( InterruptedException e ) {
            Thread.currentThread().interrupt();
        }
    }

}
