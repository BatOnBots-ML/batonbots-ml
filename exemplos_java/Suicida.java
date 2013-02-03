/*
 * Robot: Suicida
 * 
 * Procura inimigos com o radar e vai contra o primeiro que encontrar ate não ter energia.
 */

import java.io.*;
import java.util.*;


class Suicida extends Robot {
	
	public void round_started( int args ) {
		System.out.println( "round_started( " + args +  " )" );
		exec_mode("block");
        subscribe_events( "[on_hit_wall, out_of_energy, scan_event]" );
	}
	
	
	
	public void on_hit_wall( String wall ) {
		System.out.println( "on_hit_wall( " + wall + " )" );
        _hitWall = true;
	}
	
	
	public void out_of_energy() {
		System.out.println( "out_of_energy()" );
        try {
        	// Faz uma pausa para recarregar as baterias ate conseguir andar novamente
        	Thread.sleep(2000);
        }
        catch(Exception e){}
        // Reduz a velocidade para reduzir o consumo de energia
        set_speed( 2 );
        execute();
	}
	
	
	
	
	
	public void scan_event( ScanEvent event ) {
		_targets.clear();
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

			_targets.add( obj );
            counter += 1;
            System.out.println( "#################################" );
		}
	}

	
	
	
	// Enquanto true o robô continua a funcionar
	boolean alive = true;
	// Lista com os objectos encontrados durante o rastreio
	List <ObjClass>_targets = new <ObjClass>ArrayList();
	//
	boolean _hitWall = false;

	void start() {
		int direction = 0;
		int halfDist = 0;
		// Inicia o robô
		init();
        while ( alive ) {
            scan();
            execute();
            if ( !_targets.isEmpty() ) {
            	ObjClass target = null;
            	// Ataca o primeiro alvo encontrado
            	target = _targets.get(0);
            	// Direcciona-se parar o inimigo
            	robot_turn_to( (Double)target.objRelativeDirection );
                // Vai-se aproximando gradualmente
                halfDist = ( (int)target.objDistance / 2 );
                // Se estiver a bater numa parede não anda para a frente
                if ( _hitWall == true ) {
                    _hitWall = false;
                	robot_move_backward( halfDist );
            	}
                else
                    robot_move_forward( halfDist );
                execute();
            }
        }
	}
	
	
	
	
	
	

	public static void main( String[] args ) {
		Suicida robot = new Suicida();
		robot.start();
	}
	
}