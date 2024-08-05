
import serial




class Simulation:


    def __init__(self,init_function,update_function,log_function):
        self.altitude = 0
        self.long = 0
        self.lat = 0
        self.update_function = update_function
        self.log_function = log_function
        self.finished=False
        self.start_state = 1

        init_function(self)

    def update(self):
        self.update_function(self)
    

    def isFinished(self):
        return self.finished




class SimController():

    def __init__(self,com_port):
        self.currentSim = None
        self.simulations=[]
        self.com_port = com_port
        self.ser = None

        self.__has_resetted_state = True

    def enqueue_simulation(self,simulation):
        self.simulations.append(simulation)

    def __load_next_simulation(self):
        if(len(self.simulations)>0):
            self.currentSim = self.simulations.pop()
        else:
            self.currentSim = None
            
    
    def __recieved_msg(self,serial_input):

        logs = self.__simulate_sensors(serial_input)


        if(self.currentSim != None):
           
            if(logs):
               self.currentSim.log_function(logs)
        
           
    
    def __simulate_sensors(self,serial_input):
        out_str = serial_input

        sensor_value = None

        if "%STATE%" in out_str:
            
            

            out_str=out_str.replace('%STATE%', '')
            sensor_value = -1
            if self.currentSim.isFinished():
                
                if(len(self.simulations) > 0):
                    sensor_value=self.simulations[1]
                
                    
                self.__has_resetted_state = True



        
        elif "%BARO%" in out_str:
            out_str= out_str.replace('%BARO%', '')
            sensor_value = 9
        

        if(sensor_value != None):
            self.ser.write(repr(sensor_value).encode())
        
        return out_str.strip()


    def start_simulations(self):
        self.__load_next_simulation()

        self.ser = serial.Serial(
        port=self.com_port,       
        baudrate=115200,     
        timeout=0.5         
        )


        self.ser.write("3".encode()) # saying to the chip that we are online!
        try:
            while self.currentSim is not None :

                if self.currentSim.isFinished() and self.__has_resetted_state:

                        self.__load_next_simulation()
                        self.__has_resetted_state = False

                    

                if self.ser.in_waiting > 0:
                    line = self.ser.readline() #NOTE IN REAL SITUATIONS THERE IS NO NEW LINE 
                    line = line.decode().strip()
                    
                    self.__recieved_msg(line)


            
        except KeyboardInterrupt:
            print("Program terminated by user.")
        finally:
            self.ser.close()
        self.ser.close()

        print("finished simulations")






    






# real world use part, this will decode the incoming messages
def decode_log(log_entry):
    pass







