/*
 * Robot: Rastreador
 * 
 * Rastreia o campo de batalha em busca dos robôs inimigos e ataca o último que encontrar.
 */

import java.io.*;
import java.util.*;


class Rastreador extends Robot {
	
	public void round_started( int args ) {
		System.out.println( "round_started( " + args +  " )" );
		// Configura o modo de execução. Neste caso não é obrigatório porque este é o modo por defeito
        exec_mode( "lock" );
        subscribe_events( "[scan_event]" );
	}

	
	
	public void scan_event( ScanEvent event ) {
		int counter = 0;
		System.out.println( "#################################" );
		for ( int i = 0; i < event.count(); i++ ) {
			System.out.println( "- Alvo " + counter + " :" );
			ObjClass obj = event.objsList.get(i);

			System.out.println( obj.objName );
			System.out.println( obj.objEnergy );
			System.out.println( obj.objDamage );
			System.out.println( obj.objArmor );
			System.out.println( obj.objPosition );
			System.out.println( obj.objDirection );
			System.out.println( obj.objRelativeDirection );
			System.out.println( obj.objSpeed );
			System.out.println( obj.objDistance );

            counter += 1;
            System.out.println( "#################################" );
		}
		if ( event.found() ) {
			gun_turn_to( (Double)event.objsList.get(0).objRelativeDirection );
			shoot();
		}
	}

	
	
	
	// Enquanto true o robô continua a funcionar
	boolean alive = true;

	void start() {
		int direction = 0;
		// Inicia o robô
		init();
        while ( alive )
            scan();
	}
	
	
	
	
	
	

	public static void main( String[] args ) {
		Rastreador robot = new Rastreador();
		robot.start();
	}
	
}