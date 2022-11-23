Steps for Demoing:
  Pre-installation: python3 with pyserial, tkinter, and requests
  1. Change the "SSID" and "PASSWORD" part in the file [arduino_secrets.h] based
     on the wifi network that is chosen (Private network is preferred; otherwise 
     modify the initialization part in the main ino. file)
  2. Upload the [WiFiWebServer.ino] file to the arduino 33 IoT device 
  3. Open the serial monitor on the IDE to check the local IP address and open the 
     IP address in the browser to see the webpage refreshing the IMU data every sec
  4. Change the "http_req_url" in [IMUgesture_pong.py] to match the IP address 
     in the browser
  5. Run the python program [IMUgesture_pong.py] in the terminal to display the game
