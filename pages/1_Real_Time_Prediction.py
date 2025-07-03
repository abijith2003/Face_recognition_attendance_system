from Home import st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

st.set_page_config(page_title='Prediction', layout='wide')
st.subheader('Real-Time Attendance System')

# Retrieve data from Redis Database
with st.spinner('Retrieving Data from Redis DB...'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)

st.success("Data Successfully retrieved from Redis")

# Initialize time and RealTimePred class
waitTime = 30  # time in sec
setTime = time.time()
realtimepred = face_rec.RealTimePred()  # Real time prediction Class

# Callback function for real-time prediction
def video_frame_callback(frame):
    global setTime
    img = frame.to_ndarray(format="bgr24")  # 3 dimension numpy array

    # Perform face prediction
    pred_img = realtimepred.face_prediction(img, redis_face_db,
                                            'facial_features', ['Name', 'Role'], thresh=0.5)

    # Check if it's time to save logs to Redis
    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time()  # Reset Time
        print("Saving data to Redis database")

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")

# Streamlit webrtc streamer
webrtc_streamer(key="realtimeprediction", video_frame_callback=video_frame_callback)