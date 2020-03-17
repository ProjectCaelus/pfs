from enum import Enum, auto

class SensorType(Enum):
    THERMOCOUPLE = auto()
    PRESSURE = auto()
    LOAD = auto()


class SensorLocation(Enum):
    CHAMBER = auto()
    TANK = auto()
    INJECTOR = auto()


class SolenoidState(Enum):
    OPEN = auto()
    CLOSE = auto()


class SensorStatus(Enum):
    SAFE = auto()
    WARNING = auto()
    CRITICAL = auto()


class ValveType(Enum):
    SOLENOID = auto()
    BALL = auto()


class ValveLocation(Enum):
    PRESSURE_RELIEF = auto()
    PROPELLANT_VENT = auto()
    MAIN_PROPELLANT_VALVE = auto()


class ActuationType(Enum):
    PULSE = auto()
    OPEN_VENT = auto()
    CLOSE_VENT = auto()


class Stage(Enum):
    PROPELLANT_LOADING = auto()
    LEAK_TESTING_1 = auto()
    PRESSURANT_LOADING = auto()
    LEAK_TESTING_2 = auto()
    PRE_IGNITION = auto()
    DISCONNECTION = auto()