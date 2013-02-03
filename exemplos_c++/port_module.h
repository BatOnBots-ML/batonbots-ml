// http://sourceforge.net/p/predef/wiki/OperatingSystems/
#if defined(_WIN32) || defined(_WIN64) || defined(__WIN32__)
#define __WINDOWS
#include <winsock2.h>
// Multiplica por 1000 porque em linux o argumento é em segundos e em windows é em milisegundos
void sleep(int val) { Sleep(val*1000); }
#endif

#if defined(__linux) || defined(__linux__) || defined(linux)
#define __LINUX
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>     // close()
#include <arpa/inet.h>
void closesocket(int socket) { close(socket); }
#endif

#include <iostream>
#include <cstdlib>
#include <cerrno>
#include <string>
#include <cstring>
#include <sstream>
#include <vector>
#include <algorithm>
// Para o calcular em milisegundos o tempo de ping
#include <sys/timeb.h>

using namespace std;


class OnHitRobotEvent {
	/**
	 * Evento 'on_hit_robot'.
     *
     * Quando um robot embate noutro robot.
     *
     * - robotName: Nome do robot em que embateu.
     * - robotDamage: Estragods do robot em que embateu.
     * - robotArmor: vector com o estado da armadura do robot em que embateu.
     * - relativeDirection: Direcção em que o robô adversário embateu relativamente
     *                     à direcção do nosso robô. Na prática este valor é útil
     *                     para virar o robô, arma ou radar na direcção do robô em
     *                     que se embateu utilizando o comando “robot_turn_to()”,
     *                     “gun_turn_to()” ou “radar_turn_to()”.
	**/
	public:
		string robotName;
		int robotDamage;
		vector<int> robotArmor;
		float relativeDirection;

		OnHitRobotEvent( string robotName_, int robotDamage_, vector<int> robotArmor_, float relativeDirection_ ) {
			robotName = robotName_; //args.at(0);
			robotDamage = robotDamage_; //strtol( args.at(1).c_str(), NULL, 0 );
			robotArmor = robotArmor_;
			relativeDirection = relativeDirection_; //strtod( args.at(3).c_str(), NULL );
		}
};



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
	public:
		string robotName;
		float relativeDirection;

		OnHitByBulletEvent( string robotName_, float relativeDirection_ ) {
			robotName = robotName_;
			relativeDirection = relativeDirection_;
		}
};



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
	public:
		string robotName;
		int robotDamage;
		vector<int> robotArmor;
		float relativeDirection;
		float robotDistance;

		OnBulletHitEvent( string robotName_, int robotDamage_, vector<int> robotArmor_, float relativeDirection_, float robotDistance_ ) {
			robotName = robotName_; //args.at(0);
			robotDamage = robotDamage_; //strtol( args.at(1).c_str(), NULL, 0 );
			robotArmor = robotArmor_;
			relativeDirection = relativeDirection_; //strtod( args.at(3).c_str(), NULL );
			robotDistance = robotDistance_; //strtod( args.at(3).c_str(), NULL );
		}
};




class ObjClass {
	/**
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
	public:
		string objName;
		float objEnergy;
		int objDamage;
		vector<int> objArmor;
		vector<int> objPosition;
		double objDirection;
		double objRelativeDirection;
		int objSpeed;
		float objDistance;

		ObjClass( string objName_, float objEnergy_,  int objDamage_, vector<int> objArmor_, vector<int> objPosition_, float objDirection_, float objRelativeDirection_, int objSpeed_, float objDistance_ ) {
			objName = objName_;
			objEnergy = objEnergy_;
			objDamage = objDamage_;
			objArmor = objArmor_;
			objPosition = objPosition_;
			objDirection = objDirection_;
			objRelativeDirection = objRelativeDirection_;
			objSpeed = objSpeed_;
			objDistance = objDistance_;
		}
};


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
	public:
		vector<ObjClass> objsList;

		bool found () {
			/*
			 * Retorna 'true' quando foram encontrados objectos, ou 'flase' quando não foram encontrados objectos.
			 */
			if ( objsList.size() > 0 )
				return true;
			else
				return false;
		}

		ObjClass pop () {
			/*
			 * O robô pode utilizar este metodo para retirar um a um como numa stack os objectos encontrados.
			 * Quando fica sem objectos retorna uma lista vazia.
			 * Outra forma do robô vir buscar os objectos encontrados é directamente à lista.
			 * Ex.: obj = event.objsList.get(0);
			 */
			if ( objsList.size() > 0 ) {
				ObjClass retObj = objsList.front();
				objsList.erase( objsList.begin() );
				return retObj;
			}
			else
				throw "is_empty";
				//throw out_of_range;
		}

		int count () {
			/*
			 * Retorna o número de objectos encontrados.
			 */
			return objsList.size();
		}

		ScanEvent( vector<ObjClass> objVec ) {
			/*
			 * objVec = [   [ "Aleatorio", 92.1, 0, [95, 100, 70, 100], [329, 70], 69.0, 288.8, 4, 420.27 ]   ]
			 */
			objsList = objVec;
		}
};






class Robot {

    public:
        Robot();
        ~Robot();
        // Time-out para o socket
        // Nao esta a ser utilizado neste momento
        //const short TIMEOUT = 30;

		// Comandos
		short int init();
		string robot_move_forward( int val );
		string robot_move_backward( int val );
		string robot_turn_right( float val );
		string robot_turn_left( float val );
		string robot_turn_to( float val );
		//
		string gun_turn_right( float val );
		string gun_turn_left( float val );
		string gun_turn_to( float val );
		string shoot();
		//
		string radar_turn_right( float val );
		string radar_turn_left( float val );
		string radar_turn_to( float val );
		//
		string set_speed( int val );
		string scan( string direction );
		string scan();
		string advanced_scan( string direction );
		string advanced_scan();
		string no_freeze_on( string events );
		string freeze_on( string events );
		string subscribe_events( string events );
		string unsubscribe_events( string events );
		string noop();
		string stop();
		string lock_gun_on_robot( string flag );
		string lock_radar_on_robot( string flag );
		string lock_gun_on_radar( string flag );
		string exec_mode( string val );
		string execute();


		// Eventos
		virtual void done( string seqNum );
		virtual void round_started( int roundNum );
		virtual void term_battle_room();
		virtual void term_battle();
		virtual void command_dropped( vector<string> commandSet );
		virtual void invalid_arg( vector<string> commandSet );
		virtual void invalid_arg_max( vector<string> commandSet );
		virtual void destroyed( string robotName );
		virtual void kicked_robot( string robotName );
		virtual void robot_destroyed( string robotName );
		virtual void on_hit_wall( string wall );
		virtual void on_hit_robot( OnHitRobotEvent event );
		virtual void on_hit_by_bullet( OnHitByBulletEvent event );
		virtual void on_bullet_hit( OnBulletHitEvent event );
		virtual void gun_overheat();
		virtual void out_of_energy();
		virtual void scan_event( ScanEvent event );
		virtual void error( string err );


		// GetCommands
		vector<int> get_robot_position();
		vector<int> get_bf_size();
		int get_speed();
		int get_seq_num();
		float get_robot_dir();
		float get_gun_dir();
		float get_radar_dir();
		string get_exec_mode();
		vector<string> get_robots();
		vector<string> get_alive_robots();
		float get_energy();
		int get_damage();
		vector<int> get_armor();
		float get_gun_temp();
		int get_round();
		int get_round_time();
		int get_rounds_num();
		float get_elapsed_time();
		vector<string> get_no_freeze_on();
		vector<string> get_subscribed_events();
		vector< vector<string> > get_commands_queue();
		float ping();
		string get_gun_lock();
		string get_radar_lock();



    protected:
        // IP da interface loopback para estabelecer conexao com o interface.
        // Isto se o localhost estiver configurado com '127.0.0.1'
        static const char LOCALHOST[];
        //
        static const string EOL;
        // Porta da interface
        static const int PORT = 48080;
        //
        string syncData;
		// Socket utilizado na comunicacao com o interface
		int sock;
		struct sockaddr_in servAddr;
        // Buffer para o recv() do socket
        static const int BUFFER_SIZE = 1024;

		// Metodos
		vector<string> commandsList( string command, string args );
        void _shutdown();
        void _finish();
        short int _connect();
        string _recv_from_server();
        int _send_to_server( string data );
        vector<string> _command_parser( string commandSet );
		//
		bool _ends_with( string data, string end );
		bool _starts_with( string data, string end );
		vector<string> _split( string str, string sep );
		string _sync_data( string data );
		//
        vector<string> _wait_for_server();
		int count_items( string data );
		string remove_spaces( string data );
        string _eval( string data, vector<int> levels );


		// Eventos
		vector<string> _done( string args );
		vector<string> _round_started( string args );
		vector<string> _term_battle_room( string args );
		vector<string> _term_battle( string args );
		vector<string> _command_dropped( string args );
		vector<string> _invalid_arg( string args );
		vector<string> _invalid_arg_max( string args );
		vector<string> _destroyed( string args );
		vector<string> _kicked_robot( string args );
		vector<string> _robot_destroyed( string args );
		vector<string> _on_hit_wall( string args );
		vector<string> _on_hit_robot( string args );
		vector<string> _on_hit_by_bullet( string args );
		vector<string> _on_bullet_hit( string args );
		vector<string> _gun_overheat( string args );
		vector<string> _out_of_energy( string args );
		vector<string> _scan_event( string args );
		vector<string> _error( string args );


		// GetCommands
		vector<string> _get_robot_position( string args );
		vector<string> _get_bf_size( string args );
		vector<string> _get_speed( string args );
		vector<string> _get_seq_num( string args );
		vector<string> _get_robot_dir( string args );
		vector<string> _get_gun_dir( string args );
		vector<string> _get_radar_dir( string args );
		vector<string> _get_exec_mode( string args );
		vector<string> _get_robots( string args );
		vector<string> _get_alive_robots( string args );
		vector<string> _get_energy( string args );
		vector<string> _get_damage( string args );
		vector<string> _get_armor( string args );
		vector<string> _get_gun_temp( string args );
		vector<string> _get_round( string args );
		vector<string> _get_round_time( string args );
		vector<string> _get_rounds_num( string args );
		vector<string> _get_elapsed_time( string args );
		vector<string> _get_no_freeze_on( string args );
		vector<string> _get_subscribed_events( string args );
		vector<string> _get_commands_queue( string args );
		vector<string> _ping( string args );
		vector<string> _get_gun_lock( string args );
		vector<string> _get_radar_lock( string args );
};

const char Robot::LOCALHOST[] = "127.0.0.1";
const string Robot::EOL = "\r\n";
















Robot::Robot()
{
	syncData = "";
	sock = 0;
}
Robot::~Robot()
{
}



vector<string> Robot::commandsList( string command, string args ){
	vector<string> retVec;

	// ***********  Eventos  ************
	// Indica que o comando foi executado  e que pode continuar a enviar comandos.
	if( command == "done" ){
		retVec = _done( args );
	}
	// Indica que o round começou e que pode começar a enviar comandos
	else if( command == "round_started" ){
		retVec = _round_started( args );
	}
	// Quando a sala de jogo foi fechada
	else if( command == "term_battle_room" ){
		retVec = _term_battle_room( args );
	}
	// Quando a batalha termina
	else if( command == "term_battle" ){
		retVec = _term_battle( args );
	}
	// Quando um comando válido é descartado pelo servidor
	else if( command == "command_dropped" ){
		retVec = _command_dropped( args );
	}
	// Quando um comando é enviado com um argumento inválido
	else if( command == "invalid_arg_inf" ){
		retVec = _invalid_arg( args );
	}
	// Quando o robô excede o número máximo de comandos inválidos
	else if( command == "invalid_arg_max" ){
		retVec = _invalid_arg_max( args );
	}
	// Indica que foi destruido =/
	else if( command == "destroyed" ){
		retVec = _destroyed( args );
	}
	// Quando um robot é retirado da batalha
	else if( command == "kicked_robot" ){
		retVec = _kicked_robot( args );
	}
	// Recebido quando um dos outros robots é destruido
	else if( command == "robot_destroyed" ){
		retVec = _robot_destroyed( args );
	}
	// Quando embate numa parede
	else if( command == "on_hit_wall" ){
		retVec = _on_hit_wall( args );
	}
	// quando embate noutro robot
	else if( command == "on_hit_robot" ){
		retVec = _on_hit_robot( args );
	}
	// Quando é atingido por uma bala
	else if( command == "on_hit_by_bullet" ){
		retVec = _on_hit_by_bullet( args );
	}
	// Quando uma das nossas balas atinge um robot
	else if( command == "on_bullet_hit" ){
		retVec = _on_bullet_hit( args );
	}
	// Quando a arma sobreaquece
	else if( command == "gun_overheat" ){
		retVec = _gun_overheat( args );
	}
	// Quando o robot fica sem energia
	else if( command == "out_of_energy" ){
		retVec = _out_of_energy( args );
	}
	// Quando um scan é terminado ou encontra algum objecto
	else if( command == "scan_event" ){
		retVec = _scan_event( args );
	}
	//
	else if( command == "error" ){
		retVec = _error( args );
	}


	// ***********  GetCommands  ************
	else if( command == "get_robot_position" ){
		retVec = _get_robot_position( args );
	}
	else if( command == "get_bf_size" ){
		retVec = _get_bf_size( args );
	}
	else if( command == "get_speed" ){
		retVec = _get_speed( args );
	}
	else if( command == "get_seq_num" ){
		retVec = _get_seq_num( args );
	}
	else if( command == "get_robot_dir" ){
		retVec = _get_robot_dir( args );
	}
	else if( command == "get_gun_dir" ){
		retVec = _get_gun_dir( args );
	}
	else if( command == "get_radar_dir" ){
		retVec = _get_radar_dir( args );
	}
	else if( command == "get_exec_mode" ){
		retVec = _get_exec_mode( args );
	}
	else if( command == "get_robots" ){
		retVec = _get_robots( args );
	}
	else if( command == "get_alive_robots" ){
		retVec = _get_alive_robots( args );
	}
	else if( command == "get_energy" ){
		retVec = _get_energy( args );
	}
	else if( command == "get_damage" ){
		retVec = _get_damage( args );
	}
	else if( command == "get_armor" ){
		retVec = _get_armor( args );
	}
	else if( command == "get_gun_temp" ){
		retVec = _get_gun_temp( args );
	}
	else if( command == "get_round" ){
		retVec = _get_round( args );
	}
	else if( command == "get_round_time" ){
		retVec = _get_round_time( args );
	}
	else if( command == "get_rounds_num" ){
		retVec = _get_rounds_num( args );
	}
	else if( command == "get_elapsed_time" ){
		retVec = _get_elapsed_time( args );
	}
	else if( command == "get_no_freeze_on" ){
		retVec = _get_no_freeze_on( args );
	}
	else if( command == "get_subscribed_events" ){
		retVec = _get_subscribed_events( args );
	}
	else if( command == "get_commands_queue" ){
		retVec = _get_commands_queue( args );
	}
	else if( command == "ping" ){
		retVec = _ping( args );
	}
	else if( command == "get_gun_lock" ){
		retVec = _get_gun_lock( args );
	}
	else if( command == "get_radar_lock" ){
		retVec = _get_radar_lock( args );
	}
	else
		return retVec;


	return retVec;
}











void Robot::_shutdown() {
	/**
	 * Termina a conexão com o interface.
	 */
	try {
		if ( sock ) {
			closesocket( sock );
#ifdef __WINDOWS
	WSACleanup();
#endif
		}
	} catch( int e ) {
		cout << "!!! Erro em '_shutdown()'" << endl;
		cout << "!!! Descrição: " << e << endl;
	}
}


void Robot::_finish() {
	exit( 0 );
}





short int Robot::_connect() {
	/*
	 * Cria o socket para a ligação e conecta à Interface.
	 */
	cout << ">> A criar socket e a estabelecer ligação com o Interface..." << endl;
    // Socket utilizado na comunicacao com o interface

#ifdef __WINDOWS
	WORD wVersionRequested;
	wVersionRequested = MAKEWORD( 2, 0 );
	WSADATA wsaData;
	if ( WSAStartup(wVersionRequested, &wsaData) != 0 ) {
		return -1;
	}
#endif
	// Cria o socket
	sock = socket( AF_INET, SOCK_STREAM, IPPROTO_TCP );
	if ( sock < 0 )
	{
		cout << "!!! Ocorreu um erro ao criar o socket!" << endl;
		cout << "!!! Descrição: " << errno << endl;
		return -1;
	}

	servAddr.sin_family = AF_INET;
	servAddr.sin_port = htons( PORT );
	servAddr.sin_addr.s_addr = inet_addr( LOCALHOST );

	short int retVal = connect( sock, (struct sockaddr *)&servAddr, sizeof(servAddr) );
	if ( retVal != 0 ){
		cout << "!!! Ocorreu um erro a estabelecer ligação com o Interface!" << endl;
		cout << "!!! Descrição: " << errno << endl;
		if ( sock ) {
			closesocket( sock );
#ifdef __WINDOWS
	WSACleanup();
#endif
		}
		return -1;
	}

    cout << ">> Conexão estabelecida com sucesso!" << endl;
	cout << ">> Robô Online!" << endl;
    return 0;
}




string Robot::_recv_from_server()
{
	//return "on_hit_robot([ Aleatorio0, 92, [95, 100, 70, 100], 420.27 ])";
	//return "on_hit_by_bullet([ Aleatorio0, 50.45])";
	//return "on_bullet_hit([ Aleatorio0, 50, [1, 2, 3, 4], 234.54, 500.4])";
	//return "scan_event([ [Nome, 67.4, 45, [1, 2, 3, 4], [5, 6], 90.5, 200.45, 4, 543.87], [Nome2, 76.8, 54, [4, 3, 2, 1], [6, 5], 78.3, 300.55, 2, 463.87], [Nome3, 76.8, 54, [40, 30, 22, 1], [6, 5], 78.3, 300.55, 2, 463.87] ])";
	//return "get_radar_lock(on_gun)\r\n";
	// Buffer que recebe a informação enviada pelo Interface
	char buff[ BUFFER_SIZE ];
	int recvBytes = recv( sock, buff, BUFFER_SIZE, 0 );
	if ( recvBytes < 0 ) {
		cout << "!!! Ocorreu um erro em '_recv_from_server()'" << endl;
		cout << "!!! Descrição: " << errno << endl;
		return "-1";
	}
	buff[ recvBytes ] = '\0';
	return string( buff );
}



int Robot::_send_to_server( string data )
{
	int retVal = 0;
	data += EOL;
	size_t len = data.length();
	retVal = send( sock, data.c_str(), len, 0 );
	if ( retVal < 0 ) {
		cout << "!!! Ocorreu um erro em '_send_to_server()'" << endl;
		cout << "!!! Descrição: " << errno << endl;
		return -1;
	}
	return retVal;
}



vector <string> Robot::_command_parser( string commandSet ) {
	/*
	 * Separa o comando dos argumentos caso tenha.
	 * Exemplos de commandSet:
	 *  - done(3)\r\n
	 *  - ping\r\n
	 *
	 *  Retorna um vetor com o comando e o argumento
	 *  Exemplo:
	 *   - [ "done", "3" ]
	 */
	// Guarda o comando
	string command = "";
	// Guarda o argumento. Caso não tenha, mantem-se null
	string arg = "";
	// Lista que vai ser retornada com o comando e o argumento
	vector <string> retVec;

	size_t argStart = commandSet.find( "(" );
	// Se não encontrar "(" significa que não tem argumento
	if ( argStart != string::npos ) {
		size_t argEnd = commandSet.find( ")" + EOL ) - 1;
		command = commandSet.substr( 0, argStart );
		arg = commandSet.substr( (argStart + 1), (argEnd - argStart) );
		//
		retVec.insert( retVec.begin(), command );
		retVec.insert( retVec.end(), arg );
	} else {
		size_t iEOL = commandSet.find( EOL );
		command = commandSet.substr( 0, iEOL );
		//
		retVec.push_back( command );
		// Para manter o formato do retorno -> (command, arg)
		retVec.push_back( "" );
	}

	return retVec;
}




bool Robot::_ends_with ( string data, string end )
{
    if ( data.length() >= end.length() ) {
        return ( 0 == data.compare(data.length() - end.length(), end.length(), end) );
    } else {
        return false;
    }
}


bool Robot::_starts_with ( string data, string start )
{
    if ( data.length() >= start.length() ) {
        return ( 0 == data.compare(0, start.length(), start) );
    } else {
        return false;
    }
}


vector<string> Robot::_split( string str, string sep ){
	/*
		Retirado de http://www.infernodevelopment.com/perfect-c-string-explode-split
	*/
    int found;
	vector <string> retVec;
    found = str.find( sep );
    while( found != string::npos ){
        if( found > 0 ){
            retVec.push_back( str.substr(0,found) );
        }
        str = str.substr( found + EOL.length() );
        found = str.find( sep );
    }
    if( str.length() > 0 ){
        retVec.push_back( str );
    }

	return retVec;
}


string Robot::_sync_data( string data )
{
	/*
	 * Sincroniza a informação recebida pelo socket.
	 * Testes:
	 * 'command1\r\ncommand2\r\n'
	 * 'command1' + '\r\n'
	 * 'command1\r\ncommand2\r' + '\n'
	 * 'command1\r\ncommand2' + '\r' + '\n'
	 */
	vector<string> splited;

	if ( !_ends_with( data, EOL ) && (data != "") ) {
		if ( syncData == "" )
		{
			splited = _split( data, EOL );
			syncData = splited.at( (splited.size() - 1) );
			data = data.substr( 0, (data.length() - syncData.length()) );

		} // if ( synData != "" )
		else {
			splited = _split( data, EOL );
			syncData += splited.at( 0 );
			data = data.substr( splited.at(0).length(), data.length() );
			data = syncData + data;
			splited = _split( data, EOL );
			//syncData = splited.at( (splited.size() - 1) );
			// Tem o IF para quando recebe o comando e só falta o '\n' e quando o recebe vem apenas o '\n' sem mais nada a seguir.
			if ( (syncData.length() > 0) && !_ends_with( syncData, EOL ) ) {
				data = data.substr( 0, (data.length() - syncData.length()) );
			}
		}
	} // if ( !_ends_with( data, EOL ) && (data != "") ) {
	else {
		if ( syncData != "" ) {
			data = syncData + data;
			syncData = "";
		}
	}
	return data;
}




vector<string> Robot::_wait_for_server()
{
    	vector<string> retVec;
    	string data = "";
    	// Aguarda até receber alguma informação do servidor
    	data = _recv_from_server();
    	// Quando há algum erro ou a conexão é fechada
    	if ( (data == "-1") || (data == "") ) {
    		_shutdown();
    		_finish();
			retVec.insert( retVec.begin(), "" );
    		return retVec;
    	}

        // Sincroniza a informação recebida
        data = _sync_data( data );
        while ( data == "" )
            data = _sync_data( data );

    	// Separa os comandos no caso de ter recebido mais que um
    	vector<string> commands = _split( data, EOL );
    	int len = commands.size();
    	vector<string> parsedCommand;
    	for (int i = 0; i < commands.size(); i++  ) {
    		parsedCommand = _command_parser( commands.at(i) + EOL );
    		retVec = commandsList( parsedCommand.at(0), parsedCommand.at(1) );
    	}
    	return retVec;

}







int Robot::count_items( string data )
{
	int subLevels(0);
	int items(0);

	// Verifica sem tem o formato de lista Ex.: []
	if ( _starts_with(data, "[") && _ends_with(data, "]") ) {
		// Retira o "[" inicial e "]" final
		data = data.substr( 1, (data.length() - 2 ) );
	}
	else {
		cout << endl << "Formato incorrecto!" << endl;
		return -1;
	}

	for ( int i = 0; i < data.length(); i++ ) {
		if ( data.at(i) == '[' )
			subLevels++;
		else if ( data.at(i) == ']' )
			subLevels--;
			if ( i == (data.length() - 1) ) // Quando data termina com ']'
				items++;
		else if ( subLevels != 0 )
			continue;
		else if ( (data.at(i) == ',') || (i == (data.length() - 1)) )
			items++;
	}

	return items;
}

string Robot::remove_spaces( string data )
{
	data.erase( remove( data.begin(), data.end(), ' ' ), data.end() );
	return data;
}

string Robot::_eval( string data, vector<int> levels )
{
	/*
	Testes:
	levels  ->  [ 2, 0 ]
	levels  ->  [ 0, 0 ]
	levels  ->  [ 2, 1 ]
	levels  ->  [ 1, 0 ]
	data    ->  [a,[1,3,[2]],[10,30]]

	levels  ->  [ 2, 0 ]
	levels  ->  [ 2, 1 ]
	levels  ->  [ 3 ]
	data    ->  [a,[1,3,[2]],[10,30], b]


	VARS:
	- subLevel - Serve pra saber quando está dentro dos parenteses e deve ignorar as virgulas. Só são intrepertadas virgulas quando subLevel==0
	- level - Nível actual em que se encontra.
	- begin - Aponta para a posição na string em que começa o nível que se quer retirar(indicado pelo vector levels).
			  É iniciado com -1 para se saber quando foi encontrado o inicio do nível uma vez que o inicio nunca mais er negativo.

	- Retira os espaços da string data
	- Por cada nível no vector levels:
		- begin = -1
		- Verifica se a string inicia com '[' e termina com ']' e caso seja verdade retira-os
		- Percorre a string caracter a caracter. A cada caracter:
			- (level == levels[i]) && (begin < 0): // Para o nível zero
				- True:
					- True: inicia o apontador begin com a posição actual na string
			- char == '[':
				- True: incrementa o contador subLevels e passa ao caracter seguinte
			- char == ']':
				- True: derementa o contador subLevels e passa ao caracter seguinte
					- (i == (data.size() - 1)) && (level == levels[i]):
						- True: Faz o substr da data -> data = data.substr( begin, (i - begin) + 1 )
			- subLevels != 0:
				- True: Passa ao caracter seguinte
			- (char == ',') || ( i == (data.size() - 1) ):
				- begin < 0:
					- True: incrementa o contador level
						- (level == levels[i])
							- True: inicia o apontador begin com a posição actual na string + 1
					- False: Faz o substr da data -> data = data.substr( begin, (i - begin) + (i==(data.size()-1)) ) e faz break
			- else:
				- Passa ao caracter seguinte
		- Retorna a variável data
	*/
	int subLevels(0);
	int level(0);
	int begin(-1);

    // Retira os espaços em branco
	data = remove_spaces( data );

	for ( int i = 0;  i < levels.size(); i++ ) {
		begin = -1;
		level = 0;
		// Verifica sem tem o formato de lista Ex.: []
		if ( _starts_with(data, "[") && _ends_with(data, "]") ) {
		    // Retira o "[" inicial e "]" final
		    data = data.substr( 1, (data.length() - 2 ) );
		}
		else {
			cout << endl << "Formato incorrecto!" << endl;
			return "-1";
		}
		//
		for ( int ii = 0; ii < data.length(); ii++ ) {
			if ( level == levels[i] ) {
				if ( begin < 0 )
					begin = ii;
			} // if ( level == levels[i] ) {
			if ( data.at(ii) == '[' )
				subLevels++;
			else if ( data.at(ii) == ']' ) {
				subLevels--;
				if ( (ii == (data.size() - 1)) && (level == levels[i]) )
					data = data.substr( begin, (ii - begin) + 1 );
			}
			else if ( subLevels != 0 ) {
				continue;
			} // else if ( subLevels != 0 ) {
			else if ( (data.at(ii) == ',') || (ii == (data.size() - 1)) ) {
				if ( begin < 0 ) {
					level++;
					if ( level == levels[i] )
						begin = ii + 1;
				}
				else {
					data = data.substr( begin, (ii - begin) + (ii==(data.size()-1)) );
					break;
				}
			} // else if ( (data.at(ii) == ',') || (ii == (data.size() - 1)) ) {
		} // for ( int ii = 0; ii < (data.length()); ii++ ) {
	} // for ( int i = 0;  i < levels.size(); i++ ) {

	return data;
}




/**********************************************************************************************
 * 											<COMANDOS>
 **********************************************************************************************/


short int Robot::init() {
	/*
	 * Primeiro metodo a ser invocado depois de ser criada a instancia da classe.
	 */
	if ( _connect() != 0 )
		return -1;
	_wait_for_server();
	return 0;
}


string Robot::robot_move_forward( int val ) {
	/*
	 * Move o robot para a frente.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "robot_move_forward(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::robot_move_backward( int val ) {
	/*
	 * Move o robot para a frente.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "robot_move_backward(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::robot_turn_right( float val ) {
	/*
	 * Vira o robot para a direita se 'val' for positivo e para a esquerda se for negativo.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "robot_turn_right(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::robot_turn_left( float val ) {
	/*
	 * Vira o robot para a esquerda se 'val' for positivo e para a direita se for negativo.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "robot_turn_left(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::robot_turn_to( float val ) {
	/*
	 * Vira o robot para uma direcção especifica.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "robot_turn_to(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}




string Robot::gun_turn_right( float val ) {
	/*
	 * Vira a arma para a direita se 'val' for positivo e para a esquerda se for negativo.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "gun_turn_right(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::gun_turn_left( float val ) {
	/*
	 * Vira a arma para a esquerda se 'val' for positivo e para a direita se for negativo.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "gun_turn_left(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::gun_turn_to( float val ) {
	/*
	 * Vira a arma para uma direcção especifica.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "gun_turn_to(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::shoot() {
	/*
	 * Dispara.
	 */
	vector<string>retVal;
	string commandSet = "shoot";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}




string Robot::radar_turn_right( float val ) {
	/*
	 * Vira o radar para a direita se 'val' for positivo e para a esquerda se for negativo.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "radar_turn_right(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::radar_turn_left( float val ) {
	/*
	 * Vira o radar para a esquerda se 'val' for positivo e para a direita se for negativo.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "radar_turn_left(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::radar_turn_to( float val ) {
	/*
	 * Vira o radar para uma direcção especifica.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << val;
	string commandSet = "radar_turn_to(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}



string Robot::set_speed( int speed ) {
	/*
	 * Configura a velocidade a que o robot se movimenta para a frente ou para trás.
	 * Aceita apenas valores inteiros de 1 a 4 onde 1 é a velocidade mínima e  a velocidade máxima e por defeito.
	 */
	vector<string>retVal;
	stringstream ss;
	ss << speed;
	string commandSet = "set_speed(" + ss.str() + ")";
	_send_to_server( commandSet );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::scan( string direction ) {
	/*
     * Faz um scan em busca de objectos no campo de batalha. Neste caso, robots adeversarios.
     * - Aceita como argumentos(capitalização ignorada):
     *    - 'right' - No fundo não faz nada porque é o mesmo que sem argumento(sentido dos ponteiros do relógio).
     *    - 'left' - Inverte o sentido do scan, sendo iniciado para a esquerda(sentido inverso ao dos ponteiros do relógio).
     *    - 'here' - Faz um scan apenas na direcção para onde o radar está virado.
     *
     * Quando é dado sem argumento, utiliza o 'right'.
	 */
	vector<string>retVal;
	_send_to_server( "scan(" + direction + ")" );
	retVal = _wait_for_server();
	return "0";
}
string Robot::scan() {
	/*
     * Quando é dado sem argumento, utiliza o 'right'.
	 */
	vector<string>retVal;
	_send_to_server( "scan(right)" );
	retVal = _wait_for_server();
	return "0";
}


string Robot::advanced_scan( string flag ) {
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
	vector<string>retVal;
	_send_to_server( "advanced_scan(" + flag + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}
string Robot::advanced_scan() {
	/*
     * Quando é dado sem argumento, utiliza o 'on'.
	 */
	vector<string>retVal;
	_send_to_server( "advanced_scan(on)" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::no_freeze_on( string events ) {
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
	vector<string>retVal;
	_send_to_server( "no_freeze_on(" + events + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::freeze_on( string events ) {
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
	vector<string>retVal;
	_send_to_server( "freeze_on(" + events + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::subscribe_events( string events ) {
	/*
    * Serve para configurar os eventos que o robô quer receber.
    * Como argumento recebe uma string:
    *     - "all": subscreve todos os eventos.
    *     - "['on_hit_by_bullet', 'gun_overheat']"
    * IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas.
    *               Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
	*/
	vector<string>retVal;
	_send_to_server( "subscribe_events(" + events + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::unsubscribe_events( string events ) {
	/*
    * Serve para configurar os eventos que o robô não quer receber.
    * Como argumento recebe uma string:
    *     - "all": subscreve todos os eventos.
    *     - "['on_hit_by_bullet', 'gun_overheat']"
    * IMPORTATNTE!: As plicas('') são importantes. Cada nome de evento tem de estar entre pelicas.
    *               Caso contrario e dependendo de como for o erro, todo o conjunto pode ser descartado.
	*/
	vector<string>retVal;
	_send_to_server( "unsubscribe_events(" + events + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::noop() {
	/*
     * Faz reset ao contador de inactividade do robô.
     * noop -> No Operation
	 */
	vector<string>retVal;
	_send_to_server( "noop" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::stop() {
	/*
     * Imobiliza o robô
	 */
	vector<string>retVal;
	_send_to_server( "stop" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::lock_gun_on_robot( string flag ) {
	/*
     * Faz com que a arma vire junto ao robô e vice-versa.
	 */
	vector<string>retVal;
	_send_to_server( "lock_gun_on_robot(" + flag + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::lock_radar_on_robot( string flag ) {
	/*
     * Faz com que o radar vire junto ao robô e vice-versa.
	 */
	vector<string>retVal;
	_send_to_server( "lock_radar_on_robot(" + flag + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::lock_gun_on_radar( string flag ) {
	/*
     * Faz com que a arma vire junto ao radar e vice-versa.
	 */
	vector<string>retVal;
	_send_to_server( "lock_gun_on_radar(" + flag + ")" );
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::exec_mode( string val ) {
	/*
	 * Configura o modo de execução.
	 */
	vector<string>retVal;
	int result = _send_to_server( "exec_mode(" + val + ")" );
	if ( result == -1 ) {
		_shutdown();
		_finish();
		return "-1";
	}
	retVal = _wait_for_server();
		if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


string Robot::execute() {
	/*
	 * Comando que dá a ordem para executar os comandos na stack, quando se está a utilizar o modo 'block'.
	 */
	vector<string> retVal;
	int result = _send_to_server( "execute" );
	if ( result == -1 ) {
		_shutdown();
		_finish();
		return "-1";
	}
	retVal = _wait_for_server();
	if ( retVal.size() == 0 )
		return "";
	else
		return retVal.at(0);
}


 /**********************************************************************************************
 * 											</COMANDOS>
 **********************************************************************************************/






/**********************************************************************************************
 * 											<EVENTOS>
 **********************************************************************************************/



vector<string> Robot::_done( string args ) {
	/**
     * - args : Recebido pelo robot quando um comando ou um bloco de comandos é executado na totalidade.
     *         O seu argumento (seqNum) representa a sequencia de comandos quando enviado pelo servidor,
     *         'None' quando o 'done' é enviado pelo ServerInterfacee neste caso pode ser ignorado. Pode ainda
     *         ser 'invalid_arg' ou 'command_dropped'.
     *         No fundo serve para saber a que comando(s) pertence o 'done' recebido.
     *         Bastante útil no modo 'non-lock' e em casos especificod do 'block'.
     *         É incrementado a cada comando aceite pelo servidor. O que é recebido no 'done' representa o
     *         último comando que terminou a sua execução.
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	done( args );
	retVec.push_back( "done" );
	return retVec;
}
void Robot::done( string seqNum ) {
}


vector<string> Robot::_round_started( string args ) {
	/**
     * Invocado quando um novo round é iniciado.
     *
     * - args : Número do round que acabou de iniciar.
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	int roundNum = atoi( args.c_str() );
	retVec.push_back( "round_started" );
	round_started( roundNum );

	return retVec;
}
void Robot::round_started( int roundNum ) {
}


vector<string> Robot::_term_battle_room( string args ) {
	/**
     * Invocado quando a sala de jogo é terminada.
     * - args : None.
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	term_battle_room();
	retVec.push_back( "term_battle_room" );
	return retVec;
}
void Robot::term_battle_room() {
	cout << "term_battle_room()" << endl;
	exit( 0 );
}


vector<string> Robot::_term_battle( string args ) {
	/**
     * Invocado quando a sala de jogo é terminada.
     * - args : Nome da batalha.
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	term_battle();
	retVec.push_back( "term_battle" );
	return retVec;
}
void Robot::term_battle() {
	cout << "term_battle()" << endl;
	exit( 0 );
}


vector<string> Robot::_command_dropped( string args ) {
	/**
     * Quando um comando válido é descartado pelo servidor.
     * - args:
     *    - vector com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
	**/
	vector<string> retVec;
	vector<string> commandSet;
	vector<int> levels;
	for ( int i = 0; i < 2; i++ ) {
		levels.clear();
		levels.push_back(i);
		commandSet.push_back( _eval( args, levels ) );
	}
	command_dropped( commandSet );
	retVec.push_back( "command_dropped" );
	return retVec;
}
void Robot::command_dropped( vector<string> commandSet ) {
}


vector<string> Robot::_invalid_arg( string args ) {
	/**
     *Recebido quando um dos comandos enviados tem um argumento inválido.
     * - args:
     *    - string com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
	**/
	vector<string> retVec;
	vector<string> commandSet;
	vector<int> levels;
	for ( int i = 0; i < 2; i++ ) {
		levels.clear();
		levels.push_back(i);
		commandSet.push_back( _eval( args, levels ) );
	}
	invalid_arg( commandSet );
	retVec.push_back( "invalid_arg" );
	return retVec;
}
void Robot::invalid_arg( vector<string> commandSet ) {
}


vector<string> Robot::_invalid_arg_max( string args ) {
	/**
     * Recebido quando o robô envia mais de X comandos seguidos com o argumento inválido.
     * - args:
     *    - string com o comando e o seu argumentos. Ex.: [robot_turn_right, 20000]
	**/
	vector<string> retVec;
	vector<string> commandSet;
	vector<int> levels;
	for ( int i = 0; i < 2; i++ ) {
		levels.clear();
		levels.push_back(i);
		commandSet.push_back( _eval( args, levels ) );
	}
	invalid_arg_max( commandSet );
	retVec.push_back( "invalid_arg_max" );
	return retVec;
}
void Robot::invalid_arg_max( vector<string> commandSet ) {
}


vector<string> Robot::_destroyed( string args ) {
	/**
     * Recebido quando o nosso robot é destruído.
     *
     * - args : Nome do robot que destruío o nosso robot OU 'None' se o robot for destruido por embater numa parede.
	**/
	//vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	destroyed( args );
	//return retVec;
	return _wait_for_server();
}
void Robot::destroyed( string robotName ) {
}


vector<string> Robot::_kicked_robot( string args ) {
	/**
     * Recebido quando um robot é retirado da batalha.
     * Só é recebido quando a batalha está a decorrer.
     *
     * - args: Nome do robô que foi retirado.
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	kicked_robot( args );
	retVec.push_back( "kicked_robot" );
	return retVec;
}
void Robot::kicked_robot( string robotName ) {
}


vector<string> Robot::_robot_destroyed( string args ) {
	/**
     * Recebido quando um dos outros robots é destruido.
     *
     * - args : Nome do robot que foi destruído.
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	robot_destroyed( args );
	retVec.push_back( "robot_destroyed" );
	return retVec;
}
void Robot::robot_destroyed( string robotName ) {
}


vector<string> Robot::_on_hit_wall( string args ) {
	/**
     * Quando o nosso robot embate numa parede.
     *
     * - args : Parede onde embateu. top | right | bottom | left
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	on_hit_wall( args );
	retVec.push_back( "on_hit_wall" );
	return retVec;
}
void Robot::on_hit_wall( string wall ) {
}



vector<string> Robot::_on_hit_robot( string args ) {
	/**
     * Quando um robot embate noutro robot.
     *
     * - robotName: Nome do robot em que embateu.
     * - robotDamage: Estragods do robot em que embateu.
     * - robotArmor: vector com o estado da armadura do robot em que embateu.
     * - relativeDirection: Direcção em que o robô adversário embateu relativamente
     *                    à direcção do nosso robô. Na prática este valor é útil
     *                    para virar o robô, arma ou radar na direcção do robô em
     *                    que se embateu utilizando o comando “robot_turn_to()”,
     *                    “gun_turn_to()” ou “radar_turn_to()”.
	**/
	vector<string> retVec;
	vector<int> level;
	// robotName
	level.push_back( 0 );
	string robotName = _eval( args, level );
	// robotDamage
	level.clear();
	level.push_back( 1 );
	int robotDamage = strtol( _eval( args, level ).c_str(), NULL, 0 );

	// Armadura
	vector<int> robotArmor;
	for ( int i = 0; i < 4; i++ ) {
		level.clear();
		level.push_back( 2 );
		level.push_back( i );
		robotArmor.push_back( strtol(_eval( args, level ).c_str(), NULL, 0) );
	}

	// relativeDirection
	level.clear();
	level.push_back( 3 );
	float relativeDirection = strtod( _eval( args, level ).c_str(), NULL );

	// Gera o evento
	OnHitRobotEvent event = OnHitRobotEvent( robotName, robotDamage, robotArmor, relativeDirection );
	on_hit_robot( event );
	retVec.clear();
	retVec.push_back( "on_hit_robot" );
	return retVec;
}
void Robot::on_hit_robot( OnHitRobotEvent event ) {
/*
	cout << "RobotName:" << event.robotName << endl;
	cout << "RobotDamage:" << event.robotDamage << endl;
	cout << "RobotArmor:[";
	for ( int i = 0; i < event.robotArmor.size(); i++)
		cout << event.robotArmor[i] << ", ";
	cout << "]" << endl;
	cout << "RelativeDirection:" << event.relativeDirection << endl;
*/
}



vector<string> Robot::_on_hit_by_bullet( string args ) {
	/**
	 * Quando o robot é atingido por uma bala.
	 *
	 * - robotName: Nome do robot que disparou a bala.
	 * - relativeDirection: Direcção do robô que disparou a bala relativamente ao nosso robô.
	**/
	vector<string> retVec;
	vector<int> level;
	// robotName
	level.push_back( 0 );
	string robotName = _eval( args, level );
	// relativeDirection
	//level.clear();
	level.clear();
	level.push_back( 1 );
	float relativeDirection = strtod( _eval( args, level ).c_str(), NULL );

	// Gera o evento
	OnHitByBulletEvent event( robotName, relativeDirection );
	on_hit_by_bullet( event );
	retVec.clear();
	retVec.push_back( "on_hit_by_bullet" );
	return retVec;
}
void Robot::on_hit_by_bullet( OnHitByBulletEvent event ) {
/*
	cout << "RobotName:" << event.robotName << endl;
	cout << "RelativeDirection:" << event.relativeDirection << endl;
*/
}



vector<string> Robot::_on_bullet_hit( string args ) {
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
	vector<string> retVec;
	vector<int> level;
	// robotName
	level.push_back( 0 );
	string robotName = _eval( args, level );
	// robotDamage
	level.clear();
	level.push_back( 1 );
	int robotDamage = strtol( _eval( args, level ).c_str(), NULL, 0 );

	// Armadura
	vector<int> robotArmor;
	for ( int i = 0; i < 4; i++ ) {
		level.clear();
		level.push_back( 2 );
		level.push_back( i );
		robotArmor.push_back( strtol(_eval( args, level ).c_str(), NULL, 0) );
	}

	// relativeDirection
	level.clear();
	level.push_back( 3 );
	float relativeDirection = strtod( _eval( args, level ).c_str(), NULL );

	// robotDistance
	level.clear();
	level.push_back( 4 );
	float robotDistance = strtod( _eval( args, level ).c_str(), NULL );

	// Gera o evento
	OnBulletHitEvent event = OnBulletHitEvent( robotName, robotDamage, robotArmor, relativeDirection, robotDistance );
	on_bullet_hit( event );
	retVec.clear();
	retVec.push_back( "on_bullet_hit" );
	return retVec;
}
void Robot::on_bullet_hit( OnBulletHitEvent event ) {
/*
	cout << "RobotName:" << event.robotName << endl;
	cout << "RobotDamage:" << event.robotDamage << endl;
	cout << "RobotArmor:[";
	for ( int i = 0; i < event.robotArmor.size(); i++)
		cout << event.robotArmor[i] << ", ";
	cout << "]" << endl;
	cout << "RelativeDirection:" << event.relativeDirection << endl;
	cout << "RobotDistance:" << event.robotDistance << endl;
*/
}



vector<string> Robot::_gun_overheat( string args ) {
	/**
	 * Recebido quando a ara sobreaquece.
	 * - args: Null
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	gun_overheat();
	retVec.push_back( "gun_overheat" );
	return retVec;
}
void Robot::gun_overheat() {
}


vector<string> Robot::_out_of_energy( string args ) {
	/**
	 * Recebido quando o robô fica sem energia.
	 * - args: Null
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	out_of_energy();
	retVec.push_back( "out_of_energy" );
	return retVec;
}
void Robot::out_of_energy() {
}



vector<string> Robot::_scan_event( string args ) {
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
	vector<string> retVec;
	vector<int> level;
	int items = count_items( args );
	vector<ObjClass> objsVec;

	for (int i = 0; i < items; i++) {
		// robotName
		level.clear();
		level.push_back( i );
		level.push_back( 0 );
		string objName = _eval( args, level );

		// objEnergy
		level.clear();
		level.push_back( i );
		level.push_back( 1 );
		float objEnergy = strtod( _eval( args, level ).c_str(), NULL );

		// objDamage
		level.clear();
		level.push_back( i );
		level.push_back( 2 );
		int objDamage = strtol( _eval( args, level ).c_str(), NULL, 0 );

		// objArmor
		vector<int> objArmor;
		for ( int ii = 0; ii < 4; ii++ ) {
			level.clear();
			level.push_back( i );
			level.push_back( 3 );
			level.push_back( ii );
			objArmor.push_back( strtol(_eval( args, level ).c_str(), NULL, 0) );
		}

		// objPosition
		vector<int> objPosition;
		for ( int ii = 0; ii < 2; ii++ ) {
			level.clear();
			level.push_back( i );
			level.push_back( 4 );
			level.push_back( ii );
			objPosition.push_back( strtol(_eval( args, level ).c_str(), NULL, 0) );
		}

		// objDirection
		level.clear();
		level.push_back( i );
		level.push_back( 5 );
		float objDirection = strtod( _eval( args, level ).c_str(), NULL );

		// objRelativeDirection
		level.clear();
		level.push_back( i );
		level.push_back( 6 );
		float objRelativeDirection = strtod( _eval( args, level ).c_str(), NULL );

		// objSpeed
		level.clear();
		level.push_back( i );
		level.push_back( 7 );
		int objSpeed = strtol( _eval( args, level ).c_str(), NULL, 0 );

		// objDistance
		level.clear();
		level.push_back( i );
		level.push_back( 8 );
		float objDistance = strtod( _eval( args, level ).c_str(), NULL );

		// Adiciona o objecto encontrado
		objsVec.push_back( ObjClass(objName, objEnergy, objDamage, objArmor, objPosition, objDirection, objRelativeDirection, objSpeed, objDistance) );
	}

	// Gera o evento
	ScanEvent event = ScanEvent( objsVec );
	scan_event( event );
	retVec.push_back( "scan_event" );
	return retVec;
}
void Robot::scan_event( ScanEvent event ) {
/*
	int items = event.count();
	for ( int ii = 0; ii < items; ii++ ) {
		ObjClass obj = event.pop();

		cout << "RobotName:" << obj.objName << endl;
		cout << "RobotEnergy:" << obj.objEnergy << endl;
		cout << "RobotDamage:" << obj.objDamage << endl;
		cout << "RobotArmor:[";
		for ( int i = 0; i < obj.objArmor.size(); i++)
			cout << obj.objArmor[i] << ", ";
		cout << "]" << endl;
		cout << "RobotPosition:[";
		for ( int i = 0; i < obj.objPosition.size(); i++)
			cout << obj.objPosition[i] << ", ";
		cout << "]" << endl;
		cout << "objDirection:" << obj.objDirection << endl;
		cout << "RelativeDirection:" << obj.objRelativeDirection << endl;
		cout << "RobotSpeed:" << obj.objSpeed << endl;
		cout << "RobotDistance:" << obj.objDistance << endl;
	}
*/
}



vector<string> Robot::_error( string args ) {
	/**
     * Recebido quando alguma coisa corre mal no ServerInterface.
     *
     * args - String com a indicação do problema.
	**/
	vector<string> retVec;
	//retVec.insert( retVec.begin(), args );
	error( args );
	retVec.push_back( "error" );
	return retVec;
}
void Robot::error( string err ) {
}


/**********************************************************************************************
 * 											</EVENTOS>
 **********************************************************************************************/




/**********************************************************************************************
 * 											<GetCommands>
 **********************************************************************************************/

vector<string> Robot::_get_robot_position( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector<int> Robot::get_robot_position() {
	vector<string> retVal;
	vector<int> posVec;
	_send_to_server( "get_robot_position" );
	retVal = _wait_for_server();
	for ( int i = 0; i < retVal.size(); i++ )
		posVec.push_back( strtol( retVal[i].c_str(), NULL, 0 ) );
	return posVec;
}



vector<string> Robot::_get_bf_size( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector<int> Robot::get_bf_size() {
	vector<string> retVal;
	vector<int> posVec;
	_send_to_server( "get_bf_size" );
	retVal = _wait_for_server();
	for ( int i = 0; i < retVal.size(); i++ )
		posVec.push_back( strtol( retVal[i].c_str(), NULL, 0 ) );
	return posVec;
}



vector<string> Robot::_get_speed( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
int Robot::get_speed() {
	vector<string> retVal;
	_send_to_server( "get_speed" );
	retVal = _wait_for_server();
	int speed = strtol( retVal[0].c_str(), NULL, 0 );
	return speed;
}



vector<string> Robot::_get_seq_num( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
int Robot::get_seq_num() {
	vector<string> retVal;
	_send_to_server( "get_seq_num" );
	retVal = _wait_for_server();
	int seqNum = strtol( retVal[0].c_str(), NULL, 0 );
	return seqNum;
}



vector<string> Robot::_get_robot_dir( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
float Robot::get_robot_dir() {
	vector<string> retVal;
	_send_to_server( "get_robot_dir" );
	retVal = _wait_for_server();
	float dir = strtod( retVal[0].c_str(), NULL );
	return dir;
}



vector<string> Robot::_get_gun_dir( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
float Robot::get_gun_dir() {
	vector<string> retVal;
	_send_to_server( "get_gun_dir" );
	retVal = _wait_for_server();
	float dir = strtod( retVal[0].c_str(), NULL );
	return dir;
}



vector<string> Robot::_get_radar_dir( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
float Robot::get_radar_dir() {
	vector<string> retVal;
	_send_to_server( "get_radar_dir" );
	retVal = _wait_for_server();
	float dir = strtod( retVal[0].c_str(), NULL );
	return dir;
}



vector<string> Robot::_get_exec_mode( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
string Robot::get_exec_mode() {
	vector<string> retVal;
	_send_to_server( "get_exec_mode" );
	retVal = _wait_for_server();
	string execMode = retVal[0];
	return execMode;
}



vector<string> Robot::_get_robots( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector<string> Robot::get_robots() {
	vector<string> retVal;
	vector<string> robotsVec;
	_send_to_server( "get_robots" );
	robotsVec = _wait_for_server();
	return robotsVec;
}



vector<string> Robot::_get_alive_robots( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector<string> Robot::get_alive_robots() {
	vector<string> retVal;
	vector<string> robotsVec;
	_send_to_server( "get_alive_robots" );
	robotsVec = _wait_for_server();
	return robotsVec;
}



vector<string> Robot::_get_energy( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
float Robot::get_energy() {
	vector<string> retVal;
	_send_to_server( "get_energy" );
	retVal = _wait_for_server();
	float energy = strtod( retVal[0].c_str(), NULL );
	return energy;
}



vector<string> Robot::_get_damage( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
int Robot::get_damage() {
	vector<string> retVal;
	_send_to_server( "get_damage" );
	retVal = _wait_for_server();
	int damage = strtol( retVal[0].c_str(), NULL, 0 );
	return damage;
}



vector<string> Robot::_get_armor( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector<int> Robot::get_armor() {
	vector<string> retVal;
	vector<int> armorVec;
	_send_to_server( "get_armor" );
	retVal = _wait_for_server();
	for ( int i = 0; i < retVal.size(); i++ )
		armorVec.push_back( strtol( retVal[i].c_str(), NULL, 0 ) );
	return armorVec;
}



vector<string> Robot::_get_gun_temp( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
float Robot::get_gun_temp() {
	vector<string> retVal;
	_send_to_server( "get_gun_temp" );
	retVal = _wait_for_server();
	float temp = strtod( retVal[0].c_str(), NULL );
	return temp;
}



vector<string> Robot::_get_round( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
int Robot::get_round() {
	vector<string> retVal;
	_send_to_server( "get_round" );
	retVal = _wait_for_server();
	int roundNum = strtol( retVal[0].c_str(), NULL, 0 );
	return roundNum;
}



vector<string> Robot::_get_round_time( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
int Robot::get_round_time() {
	vector<string> retVal;
	_send_to_server( "get_round_time" );
	retVal = _wait_for_server();
	int roundTime = strtol( retVal[0].c_str(), NULL, 0 );
	return roundTime;
}



vector<string> Robot::_get_rounds_num( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
int Robot::get_rounds_num() {
	vector<string> retVal;
	_send_to_server( "get_rounds_num" );
	retVal = _wait_for_server();
	int roundsNum = strtol( retVal[0].c_str(), NULL, 0 );
	return roundsNum;
}



vector<string> Robot::_get_elapsed_time( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
float Robot::get_elapsed_time() {
	vector<string> retVal;
	_send_to_server( "get_elapsed_time" );
	retVal = _wait_for_server();
	float elapsedTime = strtod( retVal[0].c_str(), NULL );
	return elapsedTime;
}



vector<string> Robot::_get_no_freeze_on( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector<string> Robot::get_no_freeze_on() {
	vector<string> retVal;
	vector<string> robotsVec;
	_send_to_server( "get_no_freeze_on" );
	robotsVec = _wait_for_server();
	return robotsVec;
}



vector<string> Robot::_get_subscribed_events( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector<string> Robot::get_subscribed_events() {
	vector<string> retVal;
	vector<string> robotsVec;
	_send_to_server( "get_subscribed_events" );
	robotsVec = _wait_for_server();
	return robotsVec;
}



vector<string> Robot::_get_commands_queue( string args ) {
	vector<string> retVal;
	vector<int> levels;
	int items = count_items( args );
	for ( int i = 0; i < items; i++ ) {
		levels.clear();
		levels.push_back(i);
		retVal.push_back( _eval( args, levels ) );
	}
	return retVal;
}
vector< vector<string> > Robot::get_commands_queue() {
	vector<string> retVal;
	vector<int> levels;
	vector< vector<string> > queueVec;
	vector<string> queueVecArgs;
	_send_to_server( "get_commands_queue" );
	retVal = _wait_for_server();

	for ( int i = 0; i < retVal.size(); i++ ) {
		// Comando
		queueVecArgs.clear();
		levels.clear();
		levels.push_back(0);
		queueVecArgs.push_back( _eval( retVal[i], levels ) );
		// Args
		levels.clear();
		levels.push_back(1);
		queueVecArgs.push_back( _eval( retVal[i], levels ) );

		queueVec.push_back( queueVecArgs );
	}

	return queueVec;
}



vector<string> Robot::_ping( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
float Robot::ping() {
    timeb tb;
    ftime( &tb );
    int start = tb.millitm + (tb.time & 0xfffff) * 1000;

	_send_to_server( "ping" );
	_wait_for_server();

    timeb tb_;
    ftime( &tb_ );
    int stop = tb_.millitm + (tb_.time & 0xfffff) * 1000;
    float elapsed =  ((float)stop - start) / 1000.0;

	return (elapsed / 2.0);
}



vector<string> Robot::_get_gun_lock( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
string Robot::get_gun_lock() {
	vector<string> retVal;
	_send_to_server( "get_gun_lock" );
	retVal = _wait_for_server();
	string gunLock = retVal[0];
	return gunLock;
}



vector<string> Robot::_get_radar_lock( string args ) {
	vector<string> retVal;
	retVal.push_back( args );
	return retVal;
}
string Robot::get_radar_lock() {
	vector<string> retVal;
	_send_to_server( "get_radar_lock" );
	retVal = _wait_for_server();
	string radarLock = retVal[0];
	return radarLock;
}



/**********************************************************************************************
 * 											</GetCommands>
 **********************************************************************************************/
