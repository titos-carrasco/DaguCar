package rcr.robots.dagucar;

import gnu.io.CommPort;
import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;
import gnu.io.NoSuchPortException;
import gnu.io.PortInUseException;
import gnu.io.UnsupportedCommOperationException;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

class Serial {
    private SerialPort serialPort;
    private InputStream in;
    private OutputStream out;

    public Serial( String portName, int bauds, int timeout ) throws IOException {
        try {
            CommPortIdentifier portIdentifier = CommPortIdentifier.getPortIdentifier( portName );
            serialPort = (SerialPort)portIdentifier.open(this.getClass().getName(), timeout );
            serialPort.setSerialPortParams( bauds, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
            serialPort.setFlowControlMode( SerialPort.FLOWCONTROL_NONE);
            serialPort.enableReceiveTimeout( timeout );
            in = serialPort.getInputStream();
            out = serialPort.getOutputStream();
        } catch ( NoSuchPortException e ){
            throw new IOException( e.getMessage() );
        } catch ( PortInUseException e ){
            throw new IOException( e.getMessage() );
        } catch( UnsupportedCommOperationException e ) {
            serialPort.close();
            throw new IOException( e.getMessage() );
        } catch ( IOException e ) {
            serialPort.close();
            throw new IOException( e.getMessage() );
        }
    }

    public void Close() {
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

    public String ReadLine() throws IOException {
        // verificar timeout
        BufferedReader buffer=new BufferedReader(new InputStreamReader(in));
        return buffer.readLine();
    }

    public byte[] ReadBytes( int nbytes ) throws IllegalArgumentException, IOException {
        if(nbytes<=0){
            throw new IllegalArgumentException();
        }
        byte bytes[] = new byte[nbytes];
        int pos = 0;
        while( nbytes>0 ){
            int n = in.read( bytes, pos, nbytes );
            if( n<0 ) {
                throw new IOException("ReadBytes() recibe -1");
            }
            else if( n==0 ) {
                System.out.println("ReadBytes() recibe 0");
            }
            pos = pos + n;
            nbytes = nbytes - n;
        }
        return bytes;
    }

    public int Read1UByte() throws IOException {
        int n = in.read();
        if(n<0) {
            throw new IOException("Read1UByte() recibe -1");
        }
        return n;
    }

    public int Read2UBytes() throws IOException {
        int nh = Read1UByte();
        int nl = Read1UByte();
        return (nh<<8) + nl;
    }

    public long Read4UBytes() throws IOException {
        long nh = Read2UBytes();
        long nl = Read2UBytes();
        return (nh<<16) + nl;
    }

    public void Write( byte[] packet ) throws IOException {
        out.write( packet );
        out.flush();
    }

    public void SetReceiveTimeout( int timeout ) {
        if( timeout>0 ) {
            try {
                serialPort.enableReceiveTimeout(timeout);
            } catch ( UnsupportedCommOperationException e ) {
            }
        }
    }

    public int GetReceiveTimeout() {
        if( serialPort.isReceiveTimeoutEnabled() ){
            return serialPort.getReceiveTimeout();
        }
        else {
            return -1;
        }
    }
}
