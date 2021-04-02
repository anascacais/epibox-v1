
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

int main(int argc, char* argv[]) { // arguments: MAC address, channels, fs, afile, driftfile     
      
   // Get date and time to save as files' names
   time_t rawtime;
   struct tm * timeinfo;
   char buffer[80];
   time (&rawtime);
   timeinfo = localtime(&rawtime);
   strftime(buffer,sizeof(buffer),"%Y-%m-%d_%H-%M-%S",timeinfo);
   std::string str(buffer);

      
   // get arguments
   char* mac = argv[1]; //argv[0] is the name of the file test.txt from arv[1] on are the actual arguments
   std::string channels_str = argv[2];
   int fs = atoi(argv[3]);
   std::string afile_name = argv[4];
   std::string driftfile_name = argv[5];
   
   // transform string with channels "0 1 2 3 4 5" to vector<int> { 1, 2, 3, 4, 5 }
   std::istringstream is( channels_str );
   std::vector<int> channels( ( std::istream_iterator<int>( is ) ), ( std::istream_iterator<int>() ) );
   

   try { 
         
      //open acquisition and drift log files
      std::ofstream ofile;
      //ofile.open("data/A" + str + ".txt"); 
      ofile.open(afile_name, std::ios::app); 
      
      std::ofstream driftfile;
      driftfile.open(driftfile_name, std::ios::app); 


      puts("Connecting to device...");
      
      // use one of the lines below
      //BITalino dev("AC:67:B2:1E:83:1A");  // device MAC address (Windows and Linux)
      //BITalino dev = BITalino("20:16:12:21:39:55");
      BITalino dev = BITalino(mac);
      
      puts("Connected to device. Press Enter to exit.");

      std::string ver = dev.version();    // get device version string
      printf("BITalino version: %s\n", ver.c_str());

      dev.battery(10);  // set battery threshold (optional)

      //dev.start(1000, {0, 1, 2, 3, 4, 5});   // start acquisition of all channels at 1000 Hz
      dev.start(fs, channels); 
      
      BITalino::VFrame frames(100); // initialize the frames vector with n frames (eg: 100)
      std::cout << "done\n";
      
      auto timestamp_start = system_clock::now();
      driftfile << timestamp_start << "  " << "\n";
      
      do
      {
         dev.read(frames); // get frames from device
         
         //uint64_t usi = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::
                  //now().time_since_epoch()).count();
            
         //driftfile << timestamp << "  " << "\n";
         //std::cout << timestamp << "\n";
         
         for ( int i=0; i < frames.size(); i = i + 1) {
               printf("DATA,%d %d %d %d %d %d %d\n", frames[i].seq,
                frames[i].analog[0], frames[i].analog[1], frames[i].analog[2], frames[i].analog[3], frames[i].analog[4], frames[i].analog[5]);
               
               if (!ofile.is_open()) {
                    printf("failed to open\n");
                } else {
                    
                    std::string nseq = std::to_string(frames[i].seq);
                    std::string a1 = std::to_string(frames[i].analog[0]);
                    std::string a2 = std::to_string(frames[i].analog[1]);
                    std::string a3 = std::to_string(frames[i].analog[2]);
                    std::string a4 = std::to_string(frames[i].analog[3]);
                    std::string a5 = std::to_string(frames[i].analog[4]);
                    std::string a6 = std::to_string(frames[i].analog[5]);
                    
                    ofile << nseq << " ";
                    for (auto chn = channels.begin(); chn != channels.end(); ++chn) {
                       ofile << frames[i].analog[*chn] << " ";
                       }
                     ofile << "\n";
                }
                
          }
          //uint64_t usf = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::
                  //now().time_since_epoch()).count();
          ////std::cout << usf - usi << "us\n";
          //driftfile << usf - usi;
          
      } while (!keypressed()); // until a key is pressed
      
      auto timestamp_end = system_clock::now();
      driftfile << timestamp_end << "  " << "\n";
      
      dev.stop(); // stop acquisition
      dev.close(); 
      
      ofile.close();
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
