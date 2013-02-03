// -*- coding: UTF-8 -*-

//package port_module;

import java.io.*;
import java.util.*;
import java.net.*;
import java.lang.Math.*;



class OnHitRobotEvent {
	/**
	 * Evento 'on_hit_robot'.
     *
     * Quando um robot embate noutro robot.
     * 
     * - robotName: Nome do robot em que embateu.
     * - robotDamage: Estragods do robot em que embateu.
     * - robotArmor: lista com o estado da armadura do robot em que embateu.
     * - relativeDirection: Direcção em que o robô adversário embateu relativamente 
     *                     à direcção do nosso robô. Na prática este valor é útil 
     *                     para virar o robô, arma ou radar na direcção do robô em 
     *                     que se embateu utilizando o comando “robot_turn_to()”, 
     *                     “gun_turn_to()” ou “radar_turn_to()”.
	**/
    public String robotName = null;
    public String robotDamage = null;
    public List robotArmor = null;
    //public String relativeDirection = null;
    public double relativeDirection = 0;
    
	public OnHitRobotEvent( List args ) {
        robotName = (String)args.get(0);
        robotDamage = (String)args.get(1);
        robotArmor = (List)args.get(2);
        relativeDirection = Double.parseDouble( (String)args.get(3) );
        //relativeDirection = (String)args.get(3);
	}
}




class OnHitByBulletEvent {
	/**
	 * 
	 * Evento 'on_hit_by_bullet'.
     * 
     * Quando o robot é atingido por uma bala.
     *
     * - robotName: Nome do robot que disparou a bala.
     * - relativeDirection: Direcção do robô que disparou a bala relativamente ao nosso robô.( double )
	**/
    public String robotName = null;
    //public String relativeDirection = null;
    public double relativeDirection = 0;
    
	public OnHitByBulletEvent( List args ) {
        robotName = (String)args.get(0);
        //relativeDirection = (String)args.get(1);
        relativeDirection = Double.parseDouble( (String)args.get(1) );
	}
}



class OnBulletHitEvent {
	/**
     * Evento 'on_bullet_hit'.
     *
     * Quando uma das nossas balas atinge outro robô.
     *
     * - robotName: Nome do robot que foi atingido.
     * - robotDamage: Estragos do robot que foi atingido.
     * - robotArmor: lista com o estado da armadura do robot que foi atingido.
     * - relativeDirection: Direcção do robot que foi atingido relativamente ao nosso robô no momento da colisão.
     * - robotDistance: Distância entre o robô atingido e o nosso.
	**/
    public String robotName = null;
    public String robotDamage = null;
    public List robotArmor = null;
    //public String relativeDirection = null;
    public double relativeDirection = 0;
    public double robotDistance = 0;
    
	public OnBulletHitEvent( List args ) {
        robotName = (String)args.get(0);
        robotDamage = (String)args.get(1);
        robotArmor = (List)args.get(2);
        //relativeDirection = (String)args.get(3);
        relativeDirection = Double.parseDouble( (String)args.get(3) );
        robotDistance = Double.parseDouble( (String)args.get(4) );
	}
}



class ScanEvent {
	/**
     * Evento 'scan_event'.
     *
     * - objName: Nome do objecto que foi encontrado.
     * - objEnergy: Energia do objecto que foi encontrado.
     * - objDamage: Estragos do objecto que foi encontrado.
     * - objArmor: Armadura do objecto que foi encontrado.
     * - objPosition: Posição [x, y] do objecto que foi encontrado arredondado às centesimas.
     * - objDirection: Direcção em graus do objectos que foi encontrado.
     * - objRelativeDirection: Posição do objecto que foi encontrado relativamente à direcção do nosso robô.
     * - objSpeed: Velocidade a que o bjecto que foi encontrado se move.
     * - objDistance: Distancia do objecto encontrado em relação ao nosso robô.
	**/
	public List<ObjClass> objsList = new <ObjClass>ArrayList();
	
	
    public boolean found () {
    	/*
    	 * Retorna 'true' quando foram encontrados objectos, ou 'flase' quando não foram encontrados objectos.
    	 */
    	if ( objsList.size() > 0 )
    		return true;
    	else
    		return false;
    }
    
    
    public ObjClass pop () {
    	/*
    	 * O robô pode utilizar este metodo para retirar um a um como numa stack os objectos encontrados.
         * Quando fica sem objectos retorna uma lista vazia.
         * Outra forma do robô vir buscar os objectos encontrados é directamente à lista.
         * Ex.: obj = event.objsList.get(0);
    	 */
    	if ( objsList.size() > 0 )
    		return (ObjClass)objsList.remove(0);
    	else
    		throw new EmptyStackException();
    }
    
    
    
    public int count () {
    	/*
    	 * Retorna o número de objectos encontrados.
    	 */
    	return objsList.size();
    }
    
    
    
    
	public ScanEvent( List args ) {
		/*
		 * args = [   [ "'Aleatorio0'", 92.1, 0, [95, 100, 70, 100], [329, 70], 69.0, 288.8, 4, 420.27 ]   ]
		 */
		for ( int i = 0; i < args.size(); i++ ) {
			List obj = new ArrayList( (List)args.get(i) );
			// Tem de retirar as plicas que o python mete na string...
			String objName = new String( (String)obj.get(0) );
			ObjClass newObj = new ObjClass( objName.replaceAll("'", ""), Double.parseDouble((String)obj.get(1)), Integer.parseInt((String)obj.get(2)), (List)obj.get(3), (List)obj.get(4), Double.parseDouble((String)obj.get(5)), Double.parseDouble((String)obj.get(6)), Integer.parseInt((String)obj.get(7)), Double.parseDouble((String)obj.get(8)) );
			objsList.add( newObj );
		}
	}
}




class ObjClass {
	/*
     * - objName: Nome do objecto que foi encontrado.
     * - objEnergy: Energia do objecto que foi encontrado.
     * - objDamage: Estragos do objecto que foi encontrado.
     * - objArmor: Armadura do objecto que foi encontrado.
     * - objPosition: Posição [x, y] do objecto que foi encontrado arredondado às centesimas.
     * - objDirection: Direcção em graus do objectos que foi encontrado.
     * - objRelativeDirection: Posição do objecto que foi encontrado relativamente à direcção do nosso robô.
     * - objSpeed: Velocidade a que o bjecto que foi encontrado se move.
     * - objDistance: Distancia do objecto encontrado em relação ao nosso robô.
    */
    public String objName = null;
    public double objEnergy = 0;
    public int objDamage = 0;
    public List objArmor = null;
    public List objPosition = null;
    public double objDirection = 0;
    public double objRelativeDirection = 0;
    public int objSpeed = 0;
    public double objDistance = 0;
    
	public ObjClass( String objName, double objEnergy,  int objDamage, List objArmor, List objPosition, double objDirection, double objRelativeDirection, int objSpeed, double objDistance ) {
		this.objName = objName;
		this.objEnergy = objEnergy;
		this.objDamage = objDamage;
		this.objArmor = objArmor;
		this.objPosition = objPosition;
		this.objDirection = objDirection;
		this.objRelativeDirection = objRelativeDirection;
		this.objSpeed = objSpeed;
		this.objDistance = objDistance;
	}
}



















class Robot {
    // Socket utilizado na comunicacao com o interface
    private Socket sock = null;
    // Buffer para o recv() do socket
	private final int BUFFER_SIZE = 1024;
    // Time-out para o socket
    // Nao esta a ser utilizado neste momento
    //public static short TIMEOUT = 30;
    // IP da interface loopback para estabelecer conexao com o interface. 
    // Isto se o localhost estiver configurado com '127.0.0.1'
    private final String LOCALHOST = "localhost";
    // Porta da interface
    private final int PORT = 48080;
    //
	private final String EOL = "\r\n";
    //
	private String syncData = "";	
	
	
	
	private List commandsList( String command, String args ){
		List retList = new ArrayList();
		
		// ***********  Eventos  ************
		// Indica que o comando foi executado  e que pode continuar a enviar comandos.
		if( command.equals("done") ){
			retList = _done( args );
		}
		// Indica que o round começou e que pode começar a enviar comandos
		else if( command.equals("round_started") ){
			retList = _round_started( args );
		}
		// Quando a sala de jogo foi fechada
		else if( command.equals("term_battle_room") ){
			retList = _term_battle_room( args );
		}
		// Quando a batalha termina
		else if( command.equals("term_battle") ){
			retList = _term_battle( args );
		}
		// Quando um comando válido é descartado pelo servidor
		else if( command.equals("command_dropped") ){
			retList = _command_dropped( args );
		}
		// Quando um comando é enviado com um argumento inválido
		else if( command.equals("invalid_arg_inf") ){
			retList = _invalid_arg( args );
		}
		// Quando o robô excede o número máximo de comandos inválidos
		else if( command.equals("invalid_arg_max") ){
			retList = _invalid_arg_max( args );
		}
		// Indica que foi destruido =/
		else if( command.equals("destroyed") ){
			retList = _destroyed( args );
		}
		// Quando um robot é retirado da batalha
		else if( command.equals("kicked_robot") ){
			retList = _kicked_robot( args );
		}
		// Recebido quando um dos outros robots é destruido
		else if( command.equals("robot_destroyed") ){
			retList = _robot_destroyed( args );
		}
		// Quando embate numa parede
		else if( command.equals("on_hit_wall") ){
			retList = _on_hit_wall( args );
		}
		// quando embate noutro robot
		else if( command.equals("on_hit_robot") ){
			retList = _on_hit_robot( args );
		}
		// Quando é atingido por uma bala
		else if( command.equals("on_hit_by_bullet") ){
			retList = _on_hit_by_bullet( args );
		}
		// Quando uma das nossas balas atinge um robot
		else if( command.equals("on_bullet_hit") ){
			retList = _on_bullet_hit( args );
		}
		// Quando a arma sobreaquece
		else if( command.equals("gun_overheat") ){
			retList = _gun_overheat( args );
		}
		// Quando o robot fica sem energia
		else if( command.equals("out_of_energy") ){
			retList = _out_of_energy( args );
		}
		// Quando um scan é terminado ou encontra algum objecto
		else if( command.equals("scan_event") ){
			retList = _scan_event( args );
		}
		// 
		else if( command.equals("error") ){
			retList = _error( args );
		}
			
		
		// ***********  GetCommands  ************
		else if( command.equals("get_robot_position") ){
			retList = _get_robot_position( args );
		}
		else if( command.equals("get_bf_size") ){
			retList = _get_bf_size( args );
		}
		else if( command.equals("get_speed") ){
			retList = _get_speed( args );
		}
		else if( command.equals("get_seq_num") ){
			retList = _get_seq_num( args );
		}
		else if( command.equals("get_robot_dir") ){
			retList = _get_robot_dir( args );
		}
		else if( command.equals("get_gun_dir") ){
			retList = _get_gun_dir( args );
		}
		else if( command.equals("get_radar_dir") ){
			retList = _get_radar_dir( args );
		}
		else if( command.equals("get_exec_mode") ){
			retList = _get_exec_mode( args );
		}
		else if( command.equals("get_robots") ){
			retList = _get_robots( args );
		}
		else if( command.equals("get_alive_robots") ){
			retList = _get_alive_robots( args );
		}
		else if( command.equals("get_energy") ){
			retList = _get_energy( args );
		}
		else if( command.equals("get_damage") ){
			retList = _get_damage( args );
		}
		else if( command.equals("get_armor") ){
			retList = _get_armor( args );
		}
		else if( command.equals("get_gun_temp") ){
			retList = _get_gun_temp( args );
		}
		else if( command.equals("get_round") ){
			retList = _get_round( args );
		}
		else if( command.equals("get_round_time") ){
			retList = _get_round_time( args );
		}
		else if( command.equals("get_rounds_num") ){
			retList = _get_rounds_num( args );
		}
		else if( command.equals("get_elapsed_time") ){
			retList = _get_elapsed_time( args );
		}
		else if( command.equals("get_no_freeze_on") ){
			retList = _get_no_freeze_on( args );
		}
		else if( command.equals("get_subscribed_events") ){
			retList = _get_subscribed_events( args );
		}
		else if( command.equals("get_commands_queue") ){
			retList = _get_commands_queue( args );
		}
		else if( command.equals("ping") ){
			retList = _ping( args );
		}
		else if( command.equals("get_gun_lock") ){
			retList = _get_gun_lock( args );
		}
		else if( command.equals("get_radar_lock") ){
			retList = _get_radar_lock( args );
		}
		else
			return retList;

		
		return retList;
	}

	
	
	
	private void _shutdown() {
    	/**
    	 * Termina a conexão com o interface.
    	 */
    	try {
    		sock.close();
    		
    	} catch( IOException e ) {
    		System.err.println( "!!! Erro em '_shutdown()'" );
    		System.err.println( "!!! Descrição: " + e.getMessage() );
    	}
    	
    }
	
	
	
    private void _finish() {
    	System.exit( 0 );
    }
   
	
	
    private byte _connect() {
    	/*
    	 * Cria o socket para a ligação à Interface.
    	 */
    	try {
    		System.out.println( "\n>> A criar socket e a estabelecer ligação com o Interface..." );
    	    // Socket utilizado na comunicacao com o interface
    	    sock = new Socket( LOCALHOST, PORT );
    	    System.out.println( ">> Conexão estabelecida com sucesso!" );
    	    System.out.println( ">> Robô Online!" );
    	    return 0;
    	}catch( IOException e ) {
    		System.err.println( "!!! Ocorreu um erro ao criar o socket ou a estabelecer ligação com o Interface!" );
    		System.err.println( "!!! Descrição: " + e );
    		return -1;
    	}
    }
	

    
    private String _recv_from_server() {
    	try {
	    	DataInputStream input;
	    	input = new DataInputStream( sock.getInputStream() );
	    	// Isto não está muito bem. Vai ficar bem quando fizer o _sync_data()
			byte[] buf = new byte[ BUFFER_SIZE ];
			int bytesRead = 0;
			String data = new String("");
			
			bytesRead = input.read( buf );
			if ( bytesRead > 0 ) {
				data = new String( buf, 0, bytesRead, "UTF-8" );
			}
			return data;
			
    	} catch( IOException e ) {
    		System.err.println( "!!! Ocorreu um erro em '_recv_from_server()'" );
    		System.err.println( "!!! Descrição: " + e );
    		return "-1";
    	}
    }
	

    private int _send_to_server( String data ) {
    	try {
    		DataOutputStream output;
			output = new DataOutputStream( sock.getOutputStream() );
			output.flush();
			output.writeBytes( data + EOL );
			return 0;
			
    	} catch( IOException e ) {
    		System.err.println( "!!! Ocorreu um erro em '_send_to_server()'" );
    		System.err.println( "!!! Descrição: " + e.getMessage() );
    		return -1;
    	}
    }
    
    
    
    private List _command_parser( String commandSet ) {
    	/*
    	 * Separa o comando dos argumentos caso tenha.
    	 * Exemplos de commandSet:
    	 *  - done(3)\r\n
    	 *  - ping\r\n
    	 *  
    	 *  Retorna uma lista com o comando e o argumento
    	 *  Exemplo:
    	 *   - [ "done", "3" ]
    	 */
    	// Guarda o comando
		String command = null;
		// Guarda o argumento. Caso não tenha, mantem-se null
		String arg = null;
		// Lista que vai ser retornada com o comando e o argumento
		List retList = new ArrayList();
		
		int argStart = commandSet.indexOf( "(" );
		// Se não encontrar "(" significa que não tem argumento
		if ( argStart > -1 ) {
			int argEnd = commandSet.indexOf( ")" + EOL );
			//command = commandSet.toLowerCase().substring( 0, argStart );
			command = commandSet.substring( 0, argStart );
			//arg = commandSet.toLowerCase().substring( (argStart + 1), argEnd );
			arg = commandSet.substring( (argStart + 1), argEnd );
		} else {
			int iEOL = commandSet.indexOf( EOL );
			//command = commandSet.toLowerCase().substring( 0, iEOL );
			command = commandSet.substring( 0, iEOL );
		}
		retList.add( command );
		retList.add( arg );
		
		return retList;
    }
    
    
    
    
    
    private String _sync_data( String data ) {
    	/*
    	 * Sincroniza a informação recebida pelo socket.
    	 */
		if ( !data.endsWith(EOL) && !data.equals("") ) {
			if ( syncData.equals("") ) {
				String[] splited = data.split( EOL );
				syncData = splited[ (splited.length - 1) ];
				data = data.substring( 0, (data.length() - syncData.length()) );
			}
			else {
				String[] splited = data.split( EOL );
				syncData += splited[0];
				data = data.substring( splited[0].length(), data.length() );
				data = syncData + data;
				splited = data.split( EOL );
				syncData = splited[ (splited.length - 1) ];
				// Tem o IF para quando recebe o comando e só falta o '\r' e quando o recebe vem apenas o '\r' sem mais nada a seguir.
				if ( syncData.length() > 0 )
					data = data.substring( 0, (data.length() - syncData.length()) );
			}
		} // if ( !data.endsWith(EOL) && !data.equals("") ) {
		else {
			if ( !syncData.equals("") ) {
				data = syncData + data;
				syncData = "";
			}
		}
	
		return data;
    }
    
    

    
    
    
    
    private List _wait_for_server() {
        	List retList = new ArrayList();
        	String data = "";
        	// Aguarda até receber alguma informação do servidor
        	data = _recv_from_server();
        	// Quando há algum erro ou a conexão é fechada
        	if ( (data.equals("-1")) || (data.equals("")) ) {
        		_shutdown();
        		_finish();
        		// Apenas para não ir vazio e dar erro em alguns metodos
        		retList.add( "" );
        		return retList;
        	}
        	
            // Sincroniza a informação recebida
            data = _sync_data( data );
            while ( data.equals("") ) {
                data = _sync_data( data );
            }
            
        	// Separa os comandos no caso de ter recebido mais que um
        	String[] commands = data.split( EOL );
        	int len = commands.length;
        	List<String> parsedCommand = new<String> ArrayList();
        	for (int i = 0; i < commands.length; i++  ) {
        		parsedCommand = _command_parser( commands[i] + EOL );
        		retList = commandsList( parsedCommand.get(0), parsedCommand.get(1) );
        	}
        	return retList;
        	
        }


    
    private List _eval( String commandSet ) {
        /**
         * Idêntico ao 'eval()' em Python.
        **/
        
        // Nível de "profundidade" em que se encontra
        // Uma lista [ 1, 2, 3 ] tem nível 0
        // Uma lista [ [1, 2], 2, 3 ] tem nível 1
        // Uma lista [ [1, [2, 3] ], 2, 3 ] tem nível 2
        int level = 0;
        // Guarda o comando
        String command = null;
        // Guarda o argumento. Caso não tenha, mantem-se null
        String arg = null;
        // Lista que vai ser retornada com o comando e o argumento
        List retList = new ArrayList();
        //
        String tmpData = "";
        
        // Retira os espaços em branco
        commandSet = commandSet.replaceAll(" ", "");
        // Verifica sem tem o formato de lista Ex.: []
        if ( commandSet.startsWith("[") && commandSet.endsWith("]") ) {
            // Retira o "[" inicial e "]" final
            commandSet = commandSet.substring( 1, (commandSet.length() - 1) );
            // Percorre a string caracter a caracter
            for ( int i = 0; i <= (commandSet.length() - 1); i++ ) {
                // Procura listas dentro de listas. IMPORTANTE!: "[" é diferente de '['
                if ( commandSet.charAt(i) == '[' ) {
                    // Incrementa o nível
                    level++;
                    List newList = new ArrayList();
                    // Procura o fim da lista encontrada. Termina com ']'. IMPORTANTE!: "]" é diferente de ']'
                    for ( int ii = (i+1); ii < commandSet.length(); ii++ ) {
                        if ( commandSet.charAt(ii) == ']' ) {
                            // 
                            if ( level == 1 ) {
                                String levelData = new String( commandSet.substring( i, (ii+1) ) );
                                newList = _eval( levelData );
                                retList.add( newList );
                                i = ii;
                                level--;
                                break;
                            } // if ( level == 1 ) {
                            else {
                            	level--;
                            }

                        } // if ( commandSet.charAt(ii) == ']' ) {
                        else if ( commandSet.charAt(ii) == '[' ) {
                            // Incremente um nível
                            level++;
                        } // else if ( commandSet.charAt(ii) == '[' ) {
                    } // for ( int ii = (i+1); ii < commandSet.length(); ii++ ) {

                } // if ( commandSet.charAt(i) == '[' ) {
                // Quando chega a uma virgula adiciona o que já tinha juntado
                else if ( commandSet.charAt(i) == ',' ) {
                    if ( !tmpData.equals("") ) {
                        if ( !tmpData.equals("]") ) {
                            retList.add( tmpData );
                            tmpData = "";
                        } else
                            i++;
                    }
                }// else if ( commandSet.charAt(i) == ',' ) {
                // Vai juntando os caracteres que não são especiais
                else if ( commandSet.charAt(i) != ']' ) {
                    tmpData += commandSet.charAt(i);
                }
            } // for ( int i = 0; i <= (commandSet.length() - 1); i++ ) {
            if ( !tmpData.equals("") )
                retList.add( tmpData );
        } // if ( commandSet.startsWith("[") && commandSet.endsWith("]") ) {
        else {
            retList.clear();
            retList.add( "-1" );
            return retList;
        }
        return retList;
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    /**********************************************************************************************
     * 											<COMANDOS>
     **********************************************************************************************/

    
	public byte init() {
    	/*
    	 * Primeiro metodo a ser invocado depois de ser criada a instancia da classe.
    	 */
    	if ( _connect() != 0 )
    		return -1;
    	_wait_for_server();
    	return 0;
    }
    
    
    public String robot_move_forward( int val ) {
    	/*
    	 * Move o robot para a frente.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "robot_move_forward(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String robot_move_backward( int val ) {
    	/*
    	 * Move o robot para trás.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "robot_move_backward(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String robot_turn_right( double val ) {
    	/*
    	 * Vira o robot para a direita se 'val' for positivo e para a esquerda se for negativo.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "robot_turn_right(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String robot_turn_left( double val ) {
    	/*
    	 * Vira o robot para a esquerda se 'val' for positivo e para a direita se for negativo.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "robot_turn_left(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String robot_turn_to( double val ) {
    	/*
    	 * Vira o robot para uma direcção especifica.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "robot_turn_to(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    
    
    
    
    
    
    public String gun_turn_right( double val ) {
    	/*
    	 * Vira a arma para a direita se 'val' for positivo e para a esquerda se for negativo.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "gun_turn_right(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String gun_turn_left( double val ) {
    	/*
    	 * Vira a arma para a esquerda se 'val' for positivo e para a direita se for negativo.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "gun_turn_left(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String gun_turn_to( double val ) {
    	/*
    	 * Vira a arma para uma direcção especifica.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "gun_turn_to(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String shoot() {
    	/*
    	 * Dispara.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "shoot" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    
    
    
    
    
    
    public String radar_turn_right( double val ) {
    	/*
    	 * Vira o radar para a direita se 'val' for positivo e para a esquerda se for negativo.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "radar_turn_right(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String radar_turn_left( double val ) {
    	/*
    	 * Vira o radar para a esquerda se 'val' for positivo e para a direita se for negativo.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "radar_turn_left(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String radar_turn_to( double val ) {
    	/*
    	 * Vira o radar para uma direcção especifica.
    	 * Nota: Na verdade o argumento é do tipo float. Mas para facilitar a xecução dos comandos, ficou double
    	 * porque para ser float o robô teria de enviar os argumentos terminados com um 'f'. Ex.: 45.56f
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "radar_turn_to(" + val + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    
    
    public String set_speed( int speed ) {
    	/*
    	 * Configura a velocidade a que o robot se movimenta para a frente ou para trás.
    	 * Aceita apenas valores inteiros de 1 a 4 onde 1 é a velocidade mínima e  a velocidade máxima e por defeito.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "set_speed(" + speed + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    public String scan( String direction ) {
    	/*
         * Faz um scan em busca de objectos no campo de batalha. Neste caso, robots adeversarios.
         * - Aceita como argumentos(capitalização ignorada):
         *    - 'right' - No fundo não faz nada porque é o mesmo que sem argumento(sentido dos ponteiros do relógio).
         *    - 'left' - Inverte o sentido do scan, sendo iniciado para a esquerda(sentido inverso ao dos ponteiros do relógio).
         *    - 'here' - Faz um scan apenas na direcção para onde o radar está virado.
         *
         * Quando é dado sem argumento, utiliza o 'right'.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "scan(" + direction + ")" );
    	retVal = _wait_for_server();
    	return "0";
    }
    public String scan() {
    	/*
         * Quando é dado sem argumento, utiliza o 'right'.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "scan(right)" );
    	retVal = _wait_for_server();
    	return "0";
    }
    
    
    public String advanced_scan( String flag ) {
    	/*
         * Altera o modo de funcionamento do scan.
         * - Aceita como argumentos(capitalização ignorada):
         *    - 'off' - Valor por defeito. Faz com que o radar gere o evento scan_event e pare o robot ao primeiro
         *    objecto identificado.
         *    - 'on' - Activa o modo avançado do scan. Neste modo o scan só termina quando dá uma volta de 360º
         *    e sempre que são encontrados objectos é gerado o evento 'scan_event'.
         *
         * Quando é dado sem argumento, utiliza o 'on'.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "advanced_scan(" + flag + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    public String advanced_scan() {
    	/*
         * Quando é dado sem argumento, utiliza o 'on'.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "advanced_scan(on)" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    public String no_freeze_on( String events ) {
    	/*
        * Serve para fazer com que determinados eventos não imobilizem o robô.
        * Como argumento recebe uma string:
        *    - "all": Nenhum evento imobiliza o robô. Com a excepção de eventos como o 'out_of_energy', 'hit_on_wall',
        *             'hit_on_robot'. Os dois ultimos só param movimentos como o 'robot_move_X' ou 'robot_turn_Y'.
        * Exemplo de argumento:
        *    - "['on_hit_by_bullet', 'gun_overheat']"
        * IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
        *              Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
    	*/
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "no_freeze_on(" + events + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String freeze_on( String events ) {
    	/*
        * Serve para fazer com que determinados eventos imobilizem o robô.
        * Como argumento recebe uma string:
        *    - "all": Nenhum evento imobiliza o robô. Com a excepção de eventos como o 'out_of_energy', 'hit_on_wall',
        *             'hit_on_robot'. Os dois ultimos só param movimentos como o 'robot_move_X' ou 'robot_turn_Y'.
        * Exemplo de argumento:
        *    - "['on_hit_by_bullet', 'gun_overheat']"
        * IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
        *              Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
    	*/
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "freeze_on(" + events + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    public String subscribe_events( String events ) {
    	/*
        * Serve para configurar os eventos que o robô quer receber.
        * Como argumento recebe uma string:
        *     - "all": subscreve todos os eventos.
        *     - "['on_hit_by_bullet', 'gun_overheat']"
        * IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
        *               Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
    	*/
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "subscribe_events(" + events + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String unsubscribe_events( String events ) {
    	/*
        * Serve para configurar os eventos que o robô não quer receber.
        * Como argumento recebe uma string:
        *     - "all": subscreve todos os eventos.
        *     - "['on_hit_by_bullet', 'gun_overheat']"
        * IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas. 
        *               Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
    	*/
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "unsubscribe_events(" + events + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    public String noop() {
    	/*
         * Faz reset ao contador de inactividade do robô.
         * noop -> No Operation
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "noop" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    public String stop() {
    	/*
         * Imobiliza o robô
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "stop" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    public String lock_gun_on_robot( String flag ) {
    	/*
         * Faz com que a arma vire junto ao robô e vice-versa.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "lock_gun_on_robot(" + flag + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String lock_radar_on_robot( String flag ) {
    	/*
         * Faz com que o radar vire junto ao robô e vice-versa.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "lock_radar_on_robot(" + flag + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    public String lock_gun_on_radar( String flag ) {
    	/*
         * Faz com que a arma vire junto ao radar e vice-versa.
    	 */
    	List <String>retVal = new <String>ArrayList();
    	_send_to_server( "lock_gun_on_radar(" + flag + ")" );
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    /**********************************************************************************************
     * 											</COMANDOS>
     **********************************************************************************************/
    

    
    
    
    
    

    
        
    public String exec_mode( String val ) {
    	/*
    	 * Configura o modo de execução.
    	 */
    	List <String>retVal = new <String>ArrayList();
        int result = _send_to_server( "exec_mode(" + val + ")" );
        if ( result == -1 ) {
            _shutdown();
            _finish();
            return "-1";
        }
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }
    
    
    public String execute() {
    	/*
    	 * Comando que dá a ordem para executar os comandos na stack, quando se está a utilizar o modo 'block'.
    	 */
    	List <String>retVal = new <String>ArrayList();
        int result = _send_to_server( "execute" );
        if ( result == -1 ) {
            _shutdown();
            _finish();
            return "-1";
        }
    	retVal = _wait_for_server();
    	return retVal.get(0);
    }    
    
    

    /**********************************************************************************************
     * 											<EVENTOS>
     **********************************************************************************************/

	
	
	List _done( String args ) {
		/**
         *- args : Recebido pelo robot quando um comando ou um bloco de comandos é executado na totalidade. 
         *         O seu argumento (seqNum) representa a sequencia de comandos quando enviado pelo servidor,
         *         'None' quando o 'done' é enviado pelo ServerInterfacee neste caso pode ser ignorado. Pode ainda
         *         ser 'invalid_arg' ou 'command_dropped'.
         *         No fundo serve para saber a que comando(s) pertence o 'done' recebido. 
         *         Bastante útil no modo 'non-lock' e em casos especificod do 'block'.
         *         É incrementado a cada comando aceite pelo servidor. O que é recebido no 'done' representa o 
         *         último comando que terminou a sua execução.
		**/
		List retList = new ArrayList();
		//retList.add( args );
		done( args );
		retList.add( "done" );
		return retList;
	}
	public void done( String seqNum ) {
	}
	
	
	List _round_started( String args ) {
		/**
         * Invocado quando um novo round é iniciado.
         *
         * - args : Número do round que acabou de iniciar.
		**/
		List retList = new ArrayList();
		//retList.add( args );
		int roundNum = new Integer( args );
		round_started( roundNum );
		retList.add( "round_started" );
		return retList;
	}
	public void round_started( int roundNum ) {
	}

	
	
	List _term_battle_room( String args ) {
		/**
         * Invocado quando a sala de jogo é terminada.
         * - args : None.
		**/
		List retList = new ArrayList();
		//retList.add( args );
		term_battle_room();
		retList.add( "term_battle_room" );
		return retList;
	}
	public void term_battle_room() {
		System.out.println( "term_battle_room()" );
		System.exit( 0 );
	}
	
	
	
	List _term_battle( String args ) {
		/**
         * Invocado quando a sala de jogo é terminada.
         * - args : Nome da batalha.
		**/
		List retList = new ArrayList();
		//retList.add( args );
		term_battle();
		retList.add( "term_battle" );
		return retList;
	}
	public void term_battle() {
		System.out.println( "term_battle()" );
		System.exit( 0 );
	}

	
	
	List _command_dropped( String args ) {
		/**
         *Quando um comando válido é descartado pelo servidor.
         * - args:
         *    - lista com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
		**/
		List retList = new ArrayList();
		List commandSet = new ArrayList();
		commandSet = _eval( args );
		command_dropped( commandSet );
		retList.add( "command_dropped" );
		return retList;
	}
	public void command_dropped( List commandSet ) {
	}
	
	
	List _invalid_arg( String args ) {
		/**
         * Recebido quando um dos comandos enviados tem um argumento inválido.
         * - args:
         *    - lista com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
		**/
		List retList = new ArrayList();
		List commandSet = new ArrayList();
		commandSet = _eval( args );
		invalid_arg( commandSet );
		retList.add( "invalid_arg" );
		return retList;
	}
	public void invalid_arg( List commandSet ) {
	}
	
	
	List _invalid_arg_max( String args ) {
		/**
         *Recebido quando o robô envia mais de X comandos seguidos com o argumento inválido.
         * - args:
         *    - lista com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
		**/
		List retList = new ArrayList();
		List commandSet = new ArrayList();
		commandSet = _eval( args );
		invalid_arg_max( commandSet );
		retList.add( "invalid_arg_max" );
		return retList;
	}
	public void invalid_arg_max( List commandSet ) {
	}
	
	
	List _destroyed( String args ) {
		/**
         * Recebido quando o nosso robot é destruído.
         *
         * - args : Nome do robot que destruío o nosso robot OU 'None' se o robot for destruido por embater numa parede.
		**/
		//List retList = new ArrayList();
		//retList.add( args );
		destroyed( args );
		//retList.add( "destroyed" );
		//return retList;
		return _wait_for_server();
	}
	public void destroyed( String robotName ) {
	}
	
	
	List _kicked_robot( String args ) {
		/**
         * Recebido quando um robot é retirado da batalha.
         * Só é recebido quando a batalha está a decorrer.
         *
         * - args: Nome do robô que foi retirado.
		**/
		List retList = new ArrayList();
		//retList.add( args );
		kicked_robot( args );
		retList.add( "kicked_robot" );
		return retList;
	}
	public void kicked_robot( String robotName ) {
	}
	
	
	List _robot_destroyed( String args ) {
		/**
         * Recebido quando um dos outros robots é destruido.
         *
         * - args : Nome do robot que foi destruído.
		**/
		List retList = new ArrayList();
		//retList.add( args );
		robot_destroyed( args );
		retList.add( "robot_destroyed" );
		return retList;
	}
	public void robot_destroyed( String robotName ) {
	}
	
	
	List _on_hit_wall( String args ) {
		/**
         * Quando o nosso robot embate numa parede.
         * 
         * - args : Parede onde embateu. top | right | bottom | left
		**/
		List retList = new ArrayList();
		//retList.add( args );
		on_hit_wall( args );
		retList.add( "on_hit_wall" );
		return retList;
	}
	public void on_hit_wall( String wall ) {
	}
	
	
	List _on_hit_robot( String args ) {
		/**
         * Quando um robot embate noutro robot.
         *
         * - robotName: Nome do robot em que embateu.
         * - robotDamage: Estragods do robot em que embateu.
         * - robotArmor: lista com o estado da armadura do robot em que embateu.
         * - relativeDirection: Direcção em que o robô adversário embateu relativamente 
         *                    à direcção do nosso robô. Na prática este valor é útil 
         *                    para virar o robô, arma ou radar na direcção do robô em 
         *                    que se embateu utilizando o comando “robot_turn_to()”, 
         *                    “gun_turn_to()” ou “radar_turn_to()”.
		**/
		List retList = new ArrayList();
		List argsList = new ArrayList();
		argsList = _eval( args );
		OnHitRobotEvent event = new OnHitRobotEvent( argsList );
		on_hit_robot( event );
		retList.add( "on_hit_robot" );
		return retList;
	}
	public void on_hit_robot( OnHitRobotEvent event ) {
	}
	
	
	List _on_hit_by_bullet( String args ) {
		/**
         * Quando o robot é atingido por uma bala.
         *
         * - robotName: Nome do robot que disparou a bala.
         * - relativeDirection: Direcção do robô que disparou a bala relativamente ao nosso robô.
		**/
		List retList = new ArrayList();
		List argsList = new ArrayList();
		argsList = _eval( args );
		OnHitByBulletEvent event = new OnHitByBulletEvent( argsList );
		on_hit_by_bullet( event );
		retList.add( "on_hit_by_bullet" );
		return retList;
	}
	public void on_hit_by_bullet( OnHitByBulletEvent event ) {
	}
	
	
	List _on_bullet_hit( String args ) {
		/**
	     * Evento 'on_bullet_hit'.
	     *
	     * Quando uma das nossas balas atinge outro robô.
	     *
	     * - robotName: Nome do robot que foi atingido.
	     * - robotDamage: Estragos do robot que foi atingido.
	     * - robotArmor: lista com o estado da armadura do robot que foi atingido.
	     * - relativeDirection: Direcção do robot que foi atingido relativamente ao nosso robô no momento da colisão.
	     * - robotDistance: Distância entre o robô atingido e o nosso.
		**/
		List retList = new ArrayList();
		List argsList = new ArrayList();
		argsList = _eval( args );
		OnBulletHitEvent event = new OnBulletHitEvent( argsList );
		on_bullet_hit( event );
		retList.add( "on_bullet_hit" );
		return retList;
	}
	public void on_bullet_hit( OnBulletHitEvent event ) {
	}
	
	
	List _gun_overheat( String args ) {
		/**
		 * Recebido quando a ara sobreaquece.
		 * - args: Null
		 */
		List retList = new ArrayList();
		//retList.add( args );
		gun_overheat();
		retList.add( "gun_overheat" );
		return retList;
	}
	public void gun_overheat() {
	}
	
	
	List _out_of_energy( String args ) {
		/**
		 * Recebido quando o robô fica sem energia.
		 * - args: Null
		 */
		List retList = new ArrayList();
		//retList.add( args );
		out_of_energy();
		retList.add( "out_of_energy" );
		return retList;
	}
	public void out_of_energy() {
	}
	
	
	List _scan_event( String args ) {
		/**
		 * args = [   [ "Aleatorio", 92.1, 0, [95, 100, 70, 100], [329, 70], 69.0, 288.8, 4, 420.27 ]   ]
         * args = [   [ objName, objEnergy, objDamage, objArmor, objPosition, objDirection, objRelativeDirection, objSpeed, objDistance ]   ]
         * - objName: Nome do objecto que foi encontrado.
         * - objEnergy: Energia do objecto que ofi encontrado.
         * - objDamage: Estragos do objecto que foi encontrado.
         * - objArmor: Armadura do objecto que foi encontrado.
         * - objPosition: Posição (x, y) do objecto que foi encontrado arredondado às centesimas.
         * - objDirection: Direcção em graus do objectos que foi encontrado.
         * - objRelativeDirection: Posição do objecto que foi encontrado relativamente à direcção do nosso robot.
         * - objSpeed: Velocidade a que o bjecto que foi encontrado se move.
         * - objDistance: Distancia do objecto encontrado em relação ao nosso robot.
		**/
		List retList = new ArrayList();
		List argsList = new ArrayList();
		argsList = _eval( args );
		ScanEvent event = new ScanEvent( argsList );
		scan_event( event );
		retList.add( "scan_event" );
		return retList;
	}
	public void scan_event( ScanEvent event ) {
	}
	
	
	List _error( String args ) {
		/**
         * Recebido quando alguma coisa corre mal no ServerInterface.
         * 
         * args - String com a indicação do problema.
		**/
		List retList = new ArrayList();
		//retList.add( args );
		error( args );
		retList.add( "error" );
		return retList;
	}
	public void error( String err ) {
	}
	
	
    /**********************************************************************************************
     * 											</EVENTOS>
     **********************************************************************************************/
	
	
	
	
    /**********************************************************************************************
     * 											<GetCommands>
     **********************************************************************************************/
	
	
	private List _get_robot_position( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List<Integer> get_robot_position() {
		List retVal = new ArrayList();
		_send_to_server( "get_robot_position" );
		retVal = _wait_for_server();
		List<Integer> pos = new ArrayList();
		// Faz a conversão de tipo
		pos.add( Integer.parseInt((String)retVal.get(0)) );
		pos.add( Integer.parseInt((String)retVal.get(1)) );

		return pos;
	}
	
	
	private List _get_bf_size( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List<Integer> get_bf_size() {
		List retVal = new ArrayList();
		_send_to_server( "get_bf_size" );
		retVal = _wait_for_server();
		List<Integer> size = new ArrayList();
		// Faz a conversão de tipo
		size.add( Integer.parseInt((String)retVal.get(0)) );
		size.add( Integer.parseInt((String)retVal.get(1)) );
		return size;
	}
	
	
	private List _get_speed( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public int get_speed() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_speed" );
		retVal = _wait_for_server();
		int speed = Integer.parseInt( retVal.get(0) );
		return speed;
	}
	
	
	private List _get_seq_num( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public int get_seq_num() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_seq_num" );
		retVal = _wait_for_server();
		int speed = Integer.parseInt( retVal.get(0) );
		return speed;
	}
	
	
	private List _get_robot_dir( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public float get_robot_dir() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_robot_dir" );
		retVal = _wait_for_server();
		float dir = Float.parseFloat( retVal.get(0) );
		return dir;
	}
	
	
	private List _get_gun_dir( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public float get_gun_dir() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_gun_dir" );
		retVal = _wait_for_server();
		float dir = Float.parseFloat( retVal.get(0) );
		return dir;
	}
	
	
	private List _get_radar_dir( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public float get_radar_dir() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_radar_dir" );
		retVal = _wait_for_server();
		float dir = Float.parseFloat( retVal.get(0) );
		return dir;
	}
	
	
	private List _get_exec_mode( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public String get_exec_mode() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_exec_mode" );
		retVal = _wait_for_server();
		return retVal.get(0);
	}
	
	
	private List _get_robots( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List get_robots() {
		List retVal = new ArrayList();
		_send_to_server( "get_robots" );
		retVal = _wait_for_server();
		return retVal;
	}
	
	
	private List _get_alive_robots( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List get_alive_robots() {
		List retVal = new ArrayList();
		_send_to_server( "get_alive_robots" );
		retVal = _wait_for_server();
		return retVal;
	}
	
	
	private List _get_energy( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public float get_energy() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_energy" );
		retVal = _wait_for_server();
		float energy = Float.parseFloat( retVal.get(0) );
		return energy;
	}
	
	
	private List _get_damage( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public int get_damage() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_damage" );
		retVal = _wait_for_server();
		int damage = Integer.parseInt( retVal.get(0) );
		return damage;
	}
	
	
	private List _get_armor( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List<Integer> get_armor() {
		List retVal = new ArrayList();
		_send_to_server( "get_armor" );
		retVal = _wait_for_server();
		List<Integer> armor = new ArrayList();
		// Faz a conversão de tipo
		for ( int i = 0; i < retVal.size(); i++ ) {
			armor.add( Integer.parseInt((String)retVal.get(i)) );
		}
		return armor;
	}
	
	
	private List _get_gun_temp( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public float get_gun_temp() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_gun_temp" );
		retVal = _wait_for_server();
		float temperature = Float.parseFloat( retVal.get(0) );
		return temperature;
	}
	
	
	private List _get_round( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public int get_round() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_round" );
		retVal = _wait_for_server();
		int round = Integer.parseInt( retVal.get(0) );
		return round;
	}
	
	
	private List _get_round_time( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public int get_round_time() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_round_time" );
		retVal = _wait_for_server();
		int roundTime = Integer.parseInt( retVal.get(0) );
		return roundTime;
	}
	
	
	private List _get_rounds_num( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public int get_rounds_num() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_rounds_num" );
		retVal = _wait_for_server();
		int roundsNum = Integer.parseInt( retVal.get(0) );
		return roundsNum;
	}
	
	
	private List _get_elapsed_time( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public float get_elapsed_time() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_elapsed_time" );
		retVal = _wait_for_server();
		float elapsed = Float.parseFloat( retVal.get(0) );
		return elapsed;
	}
	
	
	private List _get_no_freeze_on( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List<String> get_no_freeze_on() {
		List retVal = new ArrayList();
		_send_to_server( "get_no_freeze_on" );
		retVal = _wait_for_server();
		return retVal;
	}
	
	
	private List _get_subscribed_events( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List<String> get_subscribed_events() {
		List retVal = new ArrayList();
		_send_to_server( "get_subscribed_events" );
		retVal = _wait_for_server();
		return retVal;
	}
	
	
	private List _get_commands_queue( String args ) {
		List retVal = new ArrayList();
		retVal = _eval( args );
		return retVal;
	}
	public List get_commands_queue() {
		List retVal = new ArrayList();
		_send_to_server( "get_commands_queue" );
		retVal = _wait_for_server();
		return retVal;
	}
	
	
	private List _ping( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public double ping() {
		List <String>retVal = new <String>ArrayList();
		double initTime = System.currentTimeMillis();
		_send_to_server( "ping" );
		retVal = _wait_for_server();
		double delay = Math.round((System.currentTimeMillis() - initTime) / 2) / 1000.0d;
		return delay;
	}
	
	
	private List _get_gun_lock( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public String get_gun_lock() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_gun_lock" );
		retVal = _wait_for_server();
		return retVal.get(0);
	}
	
	
	private List _get_radar_lock( String args ) {
		List retVal = new ArrayList();
		retVal.add( args );
		return retVal;
	}
	public String get_radar_lock() {
		List <String>retVal = new <String>ArrayList();
		_send_to_server( "get_radar_lock" );
		retVal = _wait_for_server();
		return retVal.get(0);
	}
	
	
    /**********************************************************************************************
     * 											</GetCommands>
     **********************************************************************************************/

}