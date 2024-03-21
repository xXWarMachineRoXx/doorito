import streamlit as st 
from app import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

st.set_page_config(page_title='Predictions')
st.subheader('Real-Time Attendance System')


# Retrive the data from Redis Database
with st.spinner('Retriving Data from Redis DB ...'):    
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)
    
st.success("Data sucessfully retrived from Redis")


# time 
waitTime = 30 # time in sec
setTime = time.time()
realtimepred = face_rec.RealTimePred() # real time prediction class

# Real Time Prediction
# streamlit webrtc
# callback function
def video_frame_callback(frame):
    global setTime
    
    img = frame.to_ndarray(format="bgr24") # 3 dimension numpy array
    # operation that you can perform on the array
    pred_img = realtimepred.face_prediction(img,redis_face_db,
                                        'facial_features',['Name','Role'],thresh=0.5)
    
    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time() # reset time        
        print('Save Data to redis database')
    
    # show fps on the image
        
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")

# Injecting custom JavaScript code
js_code = """
<script>
    // Part 1:
    var vid = document.querySelector("video");
    var last_media_time, last_frame_num, fps;
    var fps_rounder = [];
    var frame_not_seeked = true;
    // Part 2 (with some modifications):
    function ticker(useless, metadata) {
      var media_time_diff = Math.abs(metadata.mediaTime - last_media_time);
      var frame_num_diff = Math.abs(metadata.presentedFrames - last_frame_num);
      var diff = media_time_diff / frame_num_diff;
      if (
        diff &&
        diff < 1 &&
        frame_not_seeked &&
        fps_rounder.length < 50 &&
        vid.playbackRate === 1 &&
        document.hasFocus()
      ) {
        fps_rounder.push(diff);
        fps = Math.round(1 / get_fps_average());
        document.querySelector("p").textContent = "FPS: " + fps + ", certainty: " + fps_rounder.length * 2 + "%";
      }
      frame_not_seeked = true;
      last_media_time = metadata.mediaTime;
      last_frame_num = metadata.presentedFrames;
      vid.requestVideoFrameCallback(ticker);
    }
    vid.requestVideoFrameCallback(ticker);
    // Part 3:
    vid.addEventListener("seeked", function () {
      fps_rounder.pop();
      frame_not_seeked = false;
    });
    // Part 4:
    function get_fps_average() {
      return fps_rounder.reduce((a, b) => a + b) / fps_rounder.length;
    }
</script>
"""

# Displaying the video player
st.markdown(js_code, unsafe_allow_html=True)
webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,)