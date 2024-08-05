from flight_simulator import *






def init(sim_data):
    pass



def update(sim_data):
    pass

def log(log_data):
    if(log_data):
        print(log_data)



if __name__ == "__main__":
    sim_controller=SimController("COM6")
    sim_test=Simulation(init,update,log)

    sim_controller.enqueue_simulation(sim_test)
    sim_controller.start_simulations()




    