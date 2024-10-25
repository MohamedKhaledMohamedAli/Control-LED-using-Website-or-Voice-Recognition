#include <iostream>
#include <wiringPi.h> // To be able to configure pins of Rasspberry Pi
#include <fstream> // To be able to read or write in an external file
#include <thread> // To make delays and have multi threads
#include <atomic> // To make shared variable between threads

// Shared variable between different threads
std::atomic<bool> QuitFlag(true);

// Function to get value of the LED from the website
void request_LED(void)
{
    
    // To store value of the LED
    std::string value = "";
    
    // To store old value
    std::string old_value = "";
    
    // Loop till user terminate the program
    while(QuitFlag.load())
    {
        
        // We get the Value from the website then store it in a text file called "data.txt"
        system("curl -s https://linuxwebsite.pythonanywhere.com/files > data.txt");
        
        // Open the text file
        std::ifstream fin("data.txt");
        
        // Get the value from text file and store it
        fin >> value;
        
        // Check if the LED value has changed
        if(value != old_value)
        {
            
            // Check if the LED will be turned ON or OFF
            if(value == "1")
            {
                
                // Turn the LED ON
                digitalWrite(0, HIGH);
            }
            else if(value == "0")
            {
                
                // Turn the LED OFF
                digitalWrite(0, LOW);
            }
            
            // Update the old value
            old_value = value;
        }
    }
}

int main()
{
    
    // Setup the Pins of Raspberry Pi numbering
    wiringPiSetup();
    
    // Set the LED Pin to be Output
    pinMode(0, OUTPUT);
    
    // Initailize the LED to be OFF at Initialization
    digitalWrite(0, LOW);
    
    // Move the request function to another thread
    std::thread T1(request_LED);
    
    // Ask the User to enter any Key to terminate the program
    std::cout << "Enter any key to Quit.......\n";
    std::cin.get();
    
    // Turn the QuitFlag to false
    QuitFlag.store(false);
    
    // Wait for the thread to be finished
    if(T1.joinable())
    {
        T1.join();
    }
    
    return 0;
}