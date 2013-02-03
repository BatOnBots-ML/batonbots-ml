/*
 * Robot: Alvo
 * 
 * Permanece imóvel no campo de batalha. Útil como alvo para testes.
 */

import java.io.*;
import java.util.*;


class Alvo extends Robot {
	// Enquanto true o robô continua a funcionar
	boolean alive = true;
	
	void start() {
		// Inicia o robô
		init();
        while ( alive ) {
	        noop();
	        try {
	        	Thread.sleep(2000);
	        }
	        catch(Exception e){}
        }
	}
	
	
	public static void main( String[] args ) {
		Alvo robot = new Alvo();
		robot.start();
	}
	
}