from Home import st
from Home import face_rec

st.set_page_config(page_title='Reporting',layout ='wide')
st.subheader('Reporting')


 # Retrive logs data and show in Report.py
    # extract data from redis list
name = 'attendance:logs'
def load_logs(name,end=-1):
    logs_list = face_rec.r.lrange(name,start=0,end=end) # extract all data from the redis database
    return logs_list


# tabs to show the info
tab1 ,tab2 = st.tabs(['Registered data','Logs'])

with tab2:
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))

with tab1:    
    if st.button('Refresh Data'):
        # Retrieve data from Redis Database
        with st.spinner('Retrieving Data from Redis DB...'):
            redis_face_db = face_rec.retrive_data(name='academy:register')
            st.dataframe(redis_face_db[['Name','Role']])

