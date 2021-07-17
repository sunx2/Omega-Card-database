# Omega Card API Server

#### ( this build is still in alpha so lacking in support , we are currently planning to increase its performance )


### How to start the server

- download the binary for your system
   - server32.exe => 32 bit windows
   - server64.exe => 64 bit windows
   - server32.bin => 32 bit linux 
   - server64.bin => 64 bit linux

- download the data.json file and keep in same folder as server binary.

- Run the application
    - ./server64.exe     => for normal run, server will be created at 
        - 0.0.0.0:8085 => for linux
        - localhost:8085 => for windows
    - ./server64.exe 127.0.0.1:5000   => for providing a ip and port, you must prove both like this.
        - runs in the provided ip:port in both OS. 