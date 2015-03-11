from cflib.crazyflie import Crazyflie
from cflib.utils import callbacks
import cflib.crtp

cflib.crtp.init_drivers()
available = cflib.crtp.scan_interfaces()
crazyflie = Crazyflie()
crazyflie.connected.add_callback(crazyflie_connected)
crazyflie.open_link("radio://0/10/250K")

roll    = 0.0
pitch   = 0.0
yawrate = 0
thrust  = 12000
crazyflie.commander.send_setpoint(roll, pitch, yawrate, thrust)