/*
 * Robot: Paredes
 * 
 * Percorre o campo de batalha encostado às paredes no sentido dos ponteiros do relógio.
 */

import java.io.*;
import java.util.*;


class Paredes extends Robot {
	
	public void round_started( int args ) {
		System.out.println( "round_started( " + args +  " )" );
        subscribe_events( "[out_of_energy]" );
	}
	
	
	
	public void out_of_energy() {
		System.out.println( "out_of_energy()" );
        try {
        	Thread.sleep(1000);
        }
        catch(Exception e){}
		set_speed( 2 );
	}

	
	
	
	// Enquanto true o robô continua a funcionar
	boolean alive = true;

	void start() {
		int direction = 0;
		// Inicia o robô
		init();
        while ( alive ) {
            robot_move_forward( 1000 );
            robot_turn_to( direction );
            direction += 90;
            if ( direction == 360 )
                direction = 0;
        }
	}
	
	
	
	
	
	

	public static void main( String[] args ) {
		Paredes robot = new Paredes();
		robot.start();
	}
	
}