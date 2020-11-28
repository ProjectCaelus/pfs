
from modules.lib.enums import SensorStatus, ActuationType, ValvePriority, ValveLocation, SensorLocation, SolenoidState, SensorStatus, ValveType
from modules.lib.errors import Error
from modules.mcl.registry import Registry
from modules.mcl.flag import Flag

class PressureControl():
    def __init__(self, registry: Registry, flag: Flag):
        print("Pressure Control")
        self.registry = registry
        self.flag = flag
        

    def begin(self, config: dict):
        self.config = config
        self.active_stages = config["pressure_control"]["active_stages"]
        self.valves = config["valves"]["list"]["solenoid"]
        self.sensors = config["sensors"]["list"]["pressure"]
        self.matchups = [(SensorLocation.PT2, ValveLocation.PRESSURE_RELIEF)]

        # raise error if needed valves aren't registered
        for sensor_loc, pressure_relief_valve in self.matchups:
            if self.registry.get(("sensor_normalized", "pressure", sensor_loc))[0] == Error.KEY_ERROR:
                raise Exception("sensor at", sensor_loc, "not registered")
            if self.registry.get(("valve", "solenoid", pressure_relief_valve))[0] == Error.KEY_ERROR:
                raise Exception("pressure_relief_valve not registered")


    def execute(self):
        #stage = self.registry.get(("general", "stage"))
        #if str(stage) not in self.active_stages:
        #    return
        self.check_pressure()


    def check_pressure(self):
        #TODO: make sure that pressure relief is the right valve
        #print("PRESSURE CONTROL")
        for sensor_loc, pressure_relief_valve in self.matchups:
            if self.registry.get(("sensor_normalized", "pressure", sensor_loc))[1] > self.sensors[sensor_loc]["boundaries"]["safe"][1]:
                # print("PRESSURE TOO HIGH")
                if self.registry.get(("valve", "solenoid", pressure_relief_valve))[1] == SolenoidState.CLOSED:
                    # print("OPENING PRESSURE RELIEF")
                    self.flag.put(("solenoid", "actuation_type", pressure_relief_valve), ActuationType.OPEN_VENT)
                    self.flag.put(("solenoid", "actuation_priority", pressure_relief_valve), ValvePriority.PI_PRIORITY)

            # elif self.registry.get(("sensor_normalized", "pressure", sensor_loc))[1] < self.sensors[sensor_loc]["boundaries"]["safe"][0]:
            #     print("PRESSURE TOO LOW")
            #     if self.registry.get(("valve", "solenoid", pressurization_valve))[1] == SolenoidState.CLOSED:
            #         print("OPENING PRESSURIZATION")
            #         self.flag.put(("solenoid", "actuation_type", pressurization_valve), ActuationType.OPEN_VENT)
            #         self.flag.put(("solenoid", "actuation_priority", pressurization_valve), ValvePriority.PI_PRIORITY)


            elif self.registry.get(("sensor_status", "pressure", sensor_loc))[1] == SensorStatus.SAFE:
                if self.registry.get(("valve", "solenoid", pressure_relief_valve))[1] == SolenoidState.OPEN:
                    # print("PRESSURE SAFE AND PRV OPEN SO CLOSING PRV WITH PI_PRIORITY")
                    self.flag.put(("solenoid", "actuation_type", pressure_relief_valve), ActuationType.CLOSE_VENT)
                    self.flag.put(("solenoid", "actuation_priority", pressure_relief_valve), ValvePriority.PI_PRIORITY)

                # if self.registry.get(("valve", "solenoid", pressurization_valve))[1] == SolenoidState.OPEN:
                #     self.flag.put(("solenoid", "actuation_type", pressurization_valve), ActuationType.CLOSE_VENT)
                #     self.flag.put(("solenoid", "actuation_priority", pressurization_valve), ValvePriority.PI_PRIORITY) 
            
