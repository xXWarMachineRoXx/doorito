import streamlit as st
import redis
from zk import ZK
import os
from dotenv import load_dotenv
# center this image
left_co, cent_co,last_co = st.columns(3)
 
with left_co:
    st.image('doorito.gif',use_column_width=True)

st.title('Doorito',anchor='center')
st.text('Doorito is a simple application to connect to ZK devices and syncs to \nKredily for attendance automation.')

with st.spinner("Loading Models and Conneting to Redis db ..."):
    import face_rec
    st.success('Model loaded sucesfully')
    st.success('Redis db sucessfully connected')   
st.header('Connect to ZK Device')

load_dotenv()

# Connect to Redis Client
hostname=os.getenv('REDIS_HOST')
portnumber=os.getenv('REDIS_PORT')
password=os.getenv('REDIS_PASSWORD')
# print(hostname,portnumber,password)

r = redis.StrictRedis(host=hostname,
                      port=portnumber,
                      password=password)
class ZKDeviceController:
    def __init__(self):
        self.zk_conn = None
        self.conn = None
        self.port= os.getenv('ZK_DEVICE_PORT')

    def connect_to_device(self, IP):
        try:
            zk = ZK(IP, port=4370, timeout=5)
            self.conn = zk.connect()
            self.conn.unlock()
            self.conn.test_voice(index=2)
            st.success('ZK device successfully connected')
            self.zk_conn = zk
        except Exception as e:
            st.error('Error in connecting to ZK device: {}'.format(str(e)))
            print('\nError in connecting to ZK device: {}'.format(str(e)))
            

    def disconnect_from_device(self,IP):
        if self.conn:
            self.conn.disconnect()
            st.success('ZK device successfully disconnected')
        else:
            st.warning('ZK device is not currently connected')

    def get_attendance_data(self):
        if self.conn:
            self.zk_conn.get_attendance()
            st.success('Attendance data successfully fetched from ZK device')
        else:
            st.warning('ZK device is not currently connected')

# Create an instance of ZKDeviceController
controller = ZKDeviceController()

# Get stored connection info from Redis if available
conn_info = r.get('connection_info')

if conn_info:
    st.info("Previous Connection Info:  " + conn_info.decode())

# Collect user input
IP = st.text_input('Enter the IP address of the ZK device',value=conn_info.decode().split(' ')[-1] if conn_info.decode() else '',autocomplete='on')
col1, col2, col3 = st.columns(3)

# Check if there's an active connection
if controller.conn is not None:
    connect_button_text = 'Disconnect from ZK device'
    connect_button_func = controller.disconnect_from_device
    connect_spinner_text = 'Disconnecting from ZK device ...'
else:
    connect_button_text = 'Connect to ZK device'
    connect_button_func = controller.connect_to_device
    connect_spinner_text = 'Connecting to ZK device ...'

with col1:
    # Connect/Disconnect to/from ZK device
    if st.button(connect_button_text):
        with st.spinner(connect_spinner_text):
            connect_button_func(IP)
            # Update connection status and store connection info in Redis
            if controller.conn is not None:
                r.set('connection_info', "Connected to ZK device at IP: {}".format(IP))
            else:
                st.warning("No valid IP address provided. Connection info not stored.")

with col2:
    # Remove disconnect button when no connection
    if controller.conn is not None:
        if st.button('Disconnect from ZK device'):
            with st.spinner("Disconnecting from ZK device ..."):
                controller.disconnect_from_device()
                # Remove connection info from Redis
                r.delete('connection_info')

with col3:
    # Get attendance data
    if st.button('Get Attendance Data'):
        with st.spinner("Fetching Attendance Data ..."):
            controller.get_attendance_data()