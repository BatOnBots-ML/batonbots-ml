/* * Robot: Rastreador *  * Rastreia o campo de batalha em busca dos robôs inimigos e ataca o último que encontrar. */#include "port_module.h"class Rastreador : public Robot {	public:		Rastreador();		~Rastreador();		void start();		private:		// Enquanto true o robô continua a funcionar		bool alive;			void round_started( int args );		void scan_event( ScanEvent event );};Rastreador::Rastreador() {	alive = true;	// Inicia o robô	init();}Rastreador::~Rastreador(){}void Rastreador::round_started( int args ) {	stringstream ss;	ss << args;	cout << "round_started( " + ss.str() +  " )" << endl;	exec_mode( "lock" );	subscribe_events( "[scan_event]" );}void Rastreador::scan_event( ScanEvent event ) {	int counter = 0;	cout << "#################################" << endl;	for ( int i = 0; i < event.count(); i++ ) {		cout << "- Alvo ";		cout << counter;		cout << " :" << endl;		ObjClass obj = event.objsList.at(i);		cout << obj.objName << endl;		cout << obj.objEnergy << endl;		cout << obj.objDamage << endl;		cout << "[";		for ( int i = 0; i < obj.objArmor.size(); i++ )			cout << " " << obj.objArmor[i];		cout << " ]" << endl;		cout << "[";		for ( int i = 0; i < obj.objPosition.size(); i++ )			cout << " " << obj.objPosition[i];		cout << " ]" << endl;		cout << obj.objDirection << endl;		cout << obj.objRelativeDirection << endl;		cout << obj.objSpeed << endl;		cout << obj.objDistance << endl;		counter += 1;		cout << "#################################" << endl;	}	if ( event.found() ) {		gun_turn_to( event.objsList.at(0).objRelativeDirection );		shoot();	}}void Rastreador::start() {	int direction = 0;	while ( alive )		scan();}int main() {	Rastreador robot;	robot.start();	return 0;}