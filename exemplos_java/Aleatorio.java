/*
 * Robot: Aleatorio
 * 
 * Movimenta-se aleatóriamente pelo campo de batalha.
 */

import java.io.*;
import java.util.*;


class Aleatorio extends Robot {
	
	public void round_started( int args ) {
		System.out.println( "round_started( " + args +  " )" );
		moving = 1;
        exec_mode("block");
        subscribe_events( "[on_hit_robot, on_hit_wall]" );
	}
	
	
	
	public void on_hit_wall( String wall ) {
		System.out.println( "on_hit_wall( " + wall + " )" );
		moving *= -1;
	}
	
	public void on_hit_robot( OnHitRobotEvent event ) {
		System.out.println( "#################################" );
		System.out.println( "on_hit_robot()" );
		System.out.println( event.robotName );
		System.out.println( event.robotDamage );
		System.out.println( event.robotArmor );
		System.out.println( event.relativeDirection );
		System.out.println( "#################################" );
		moving *= -1;
	}
	

	
	
	
	// Enquanto true o robô continua a funcionar
	boolean alive = true;
	// Controla a direcção do movimento do robô
	int moving = 1;	

	void start() {
		// Inicia o robô
		init();
        while ( alive ) {
	        robot_move_forward( 300 * moving );
	        robot_turn_right( 90 );
	        execute();
        }
	}
	
	
	
	
	
	

	public static void main( String[] args ) {
		Aleatorio robot = new Aleatorio();
		robot.start();
	}
	
}