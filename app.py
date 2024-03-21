import streamlit as st
from zk import ZK, const

st.set_page_config(page_title='Attendance System',layout='wide')
conn = None

st.header('Attendance System using Face Recognition')

with st.spinner("Loading Models and Conneting to Redis db ..."):
    import face_rec
    
st.success('Model loaded sucesfully')
st.success('Redis db sucessfully connected')
IP=st.text_input('Enter the IP address of the ZK device')
if st.button('Connect to ZK device'):
    with st.spinner("Connecting to ZK device ..."):
        try:
            zk = ZK('192.168.2.201', port=4370, timeout=5)
            # st.__loader__(zk.connect())
            conn = zk.connect()
            conn.unlock()
            conn.test_voice(index=2)
            print('door unlocked?')
        except Exception as e:
            print( "Process terminate : {}".format(e))
            st.error('Error in connecting to ZK device:'+ str(e))
            st.stop()
        finally:
            if conn:
                st.success('ZK device sucessfully connected')
            
    
            
if st.button('Disconnect to ZK device'):
    if conn:
        conn.disconnect()

    
   