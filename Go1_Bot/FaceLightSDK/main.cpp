#include "FaceLightClient.h"

int main(){
    FaceLightClient client;

    client.setAllLed(client.white);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.red);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.green);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.blue);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.yellow);
    client.sendCmd();
    usleep(500000);
    client.setAllLed(client.black);
    client.sendCmd();

    return 0;
}