import ctypes
import os




# Load DLLs
zkemsdk = ctypes.WinDLL("./zkemsdk.dll")
commpro = ctypes.WinDLL(os.path.abspath("./commpro.dll"))
comms = ctypes.WinDLL(os.path.abspath("./comms.dll"))
zkemkeeper = ctypes.WinDLL(os.path.abspath("./zkemkeeper.dll"))
tcpcomm = ctypes.WinDLL(os.path.abspath("./tcpcomm.dll"))

# Define Z_ReadRTLog function prototype
Z_ReadRTLog = zkemsdk.Z_ReadRTLog
Z_ReadRTLog.restype = ctypes.c_int

# Define Z_Connect_NET function prototype
Z_Connect_NET = zkemsdk.Z_Connect_NET
Z_Connect_NET.restype = ctypes.c_int
Z_Connect_NET.argtypes = [ctypes.c_char_p, ctypes.c_int]

# Define Z_GetDeviceInfo function prototype
Z_GetDeviceInfo = zkemsdk.Z_GetDeviceInfo
Z_GetDeviceInfo.restype = ctypes.c_int
Z_GetDeviceInfo.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

# Connect to the device
address = b"192.168.2.201"  # Example IP address of the attendance device
port = 4370  # Example port number
result_connect = Z_Connect_NET(address, port)

# Check the connection result
if result_connect == 0:
    print("Connected to the device successfully.")
else:
    print("Failed to connect to the device.")

# Define the prototype of the EMBUDP_INIT function
EMBUDP_INIT = tcpcomm.EMBUDP_INIT
EMBUDP_INIT.restype = ctypes.c_int  # Return type is int
EMBUDP_INIT.argtypes = [ctypes.c_char_p, ctypes.c_int]  # Arguments: address (string), port (int)



# Initialize communication with the TCP device
address = b"192.168.2.201"  # Example IP address of the TCP device (change this to the actual IP address)
port = 4370  # Example port number (change this to the actual port number)
result_init = EMBUDP_INIT(address, port)

# Get device information
device_info_buffer = ctypes.create_string_buffer(1024)  # Buffer to store device information
result_device_info = Z_GetDeviceInfo(result_init, device_info_buffer)

# Check the device info result
if result_device_info == 1: 
    device_info = device_info_buffer.value.decode('utf-8')  # Convert byte buffer to string
    print("Device information:", device_info)
else:   
    print("Failed to retrieve device information.")

# Read the latest attendance logs
result_read_log = Z_ReadRTLog()
if result_read_log == 1:
    print("Attendance data read successfully.")
else:
    print("Failed to read attendance data.")
