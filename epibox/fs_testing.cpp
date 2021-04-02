#include "bitalino.h"

#include <stdio.h>

#ifdef _WIN32

#include <conio.h>


bool keypressed(void)
{
	return (_kbhit() != 0);
}

#else // Linux or Mac OS

#include <sys/select.h>
#include <chrono>
#include <thread>
#include <fstream>
#include <ctime>
#include <sstream>
#include <iterator>
#include <iostream>
#include <sys/time.h>
#include <unistd.h>
#include "date.h"

using namespace date;
using namespace std::chrono;

bool keypressed(void)
{
   fd_set   readfds;
   FD_ZERO(&readfds);
   FD_SET(0, &readfds);

   timeval  readtimeout;
   readtimeout.tv_sec = 0;
   readtimeout.tv_usec = 0;

   return (select(FD_SETSIZE, &readfds, NULL, NULL, &readtimeout) == 1);
}

#endif

int main(int argc, char* argv[]) { // arguments: MAC address, channels, fs, frames
   
   // get arguments
   char* mac = argv[1]; //argv[0] is the name of the file test.txt from arv[1] on are the actual arguments
   std::string channels_str = argv[2];
   char* fs_char = argv[3];
   int fs = atoi(fs_char);
   char* frames_char = argv[4];
   int frames = atoi(frames_char);
   
   std::string fs_str(fs_char);
   std::string frames_str(frames_char);
   
   // transform string with channels "0 1 2 3 4 5" to vector<int> { 1, 2, 3, 4, 5 }
   std::istringstream is( channels_str );
   std::vector<int> channels( ( std::istream_iterator<int>( is ) ), ( std::istream_iterator<int>() ) );
   
   
   try { 
      
      std::ofstream driftfile;
      driftfile.open("/home/pi/Documents/drift_fs"+fs_str+"_frames"+frames_str+".txt", std::ios::app); 


      puts("Connecting to device...");
      
      // use one of the lines below
      //BITalino dev("AC:67:B2:1E:83:1A");  // device MAC address (Windows and Linux)
      BITalino dev = BITalino(mac);
      
      puts("Connected to device. Press Enter to exit.");

      //std::string ver = dev.version();    // get device version string
      //printf("BITalino version: %s\n", ver.c_str());

      //dev.battery(10);  // set battery threshold (optional)

      //dev.start(1000, {0, 1, 2, 3, 4, 5});   // start acquisition of all channels at 1000 Hz
      dev.start(fs, channels); 
      
      BITalino::VFrame frames(frames); // initialize the frames vector with n frames (eg: 100)
      
      do
      {
         dev.read(frames); // get frames from device
                  
         auto timestamp = system_clock::now();
         driftfile << timestamp << " " << "/n";
         
          
      } while (!keypressed()); // until a key is pressed

      dev.stop(); // stop acquisition
      dev.close(); 
      
      
      driftfile.close();
      
      printf("process stoped\n");
      std::this_thread::sleep_for(std::chrono::milliseconds(60*10));
      printf("");
      
   } // dev is destroyed here (it goes out of scope)
   catch(BITalino::Exception &e) {
      printf("BITalino exception: %s\n", e.getDescription());
      std::this_thread::sleep_for(std::chrono::milliseconds(60*10));
      printf("");
   }
   
   return 0;
}
