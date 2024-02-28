import streamlit as st
import pandas as pd
import pickle5 as pickle

def classify_blood_pressure(systolic, diastolic):
    if (systolic <= 120 and diastolic <= 80) or (systolic <= 119 and diastolic <= 77):
        return 3 #'Normal Blood Pressure'
    elif (121 <= systolic <= 129 and diastolic <= 84) or (81 <= diastolic <= 89):
        return 0 #'Elevated Blood Pressure'
    elif systolic >= 140 or diastolic >= 90:
        return 1 #'High Blood Pressure (Hypertension)'
    else:
        return 4 #other
    
def recommendation(prediction):
    st.subheader('Recommendations')
    st.info("This application serves as a tool to aid medical professionals in diagnosing conditions, however, it should not be relied upon as a replacement for professional diagnosis.")
    if prediction == 2:
        st.markdown("1. Limit daytime naps. 💤 \n2. Engage in regular physical activity.🤸‍♀️  \n3. Seek professional advice if sleep problems persist. 👩🏽‍⚕️ \n4. Limit caffeine intake before bed. ☕️\n5. Practice stress-relief techniques. 🧘🏼\n6. Avoid large meals and excessive liquids before bedtime. 🍔\n7. Create a calming bedtime routine. 🛌")
    elif prediction == 1:
        st.markdown("1. Follow up regularly with a sleep specialist.👩🏽‍⚕️  \n2. Use continuous positive airway pressure (CPAP) therapy as prescribed. 📝  \n3. Sleep on your side rather than your back. 🛌\n4. Avoid alcohol and sedatives, which can relax throat muscles. 🥂\n5. Maintain a healthy weight to reduce airway obstruction. 💪🏾\n6. Healthy lifestyle changes. 📈\n7. Elevate your head while sleeping. 🛌🏾")
    else:
        st.markdown("1. Establish a consistent sleep schedule.📆  \n2. Create a relaxing bedtime routine.💆🏽  \n3. Limit screen time before bed.💻\n4. Maintain a comfortable sleep environment. 🔇\n5. Limit daytime naps. 💤\n6. Limit caffeine intake before bed. ☕️\n7. Consider professional help if insomnia persists. 👩🏽‍⚕️")


def sidebar():
    st.sidebar.header('Parameters')
    st.sidebar.write('Please put the correct value in each')

    g =  ['Male', 'Female']
    g1 = [1, 0]
    mapping_gender = dict(zip(g,g1))
    select_gender = st.sidebar.selectbox("Gender",g)
    mapping1 = mapping_gender[select_gender]

    a = ['20s', '30s', '40s', '50s']
    a1 = [0, 1, 2, 3]
    mapping_age = dict(zip(a,a1))
    select_age = st.sidebar.selectbox("Age",a)
    mapping2 = mapping_age[select_age]

    o = ['Software Engineer', 'Doctor', 'Sales Representative', 'Teacher',
       'Nurse', 'Engineer', 'Accountant', 'Scientist', 'Lawyer',
       'Salesperson', 'Manager']
    o1 = [ 9,  1,  6, 10,  5,  2,  0,  8,  3,  7,  4]
    mapping_Occupation = dict(zip(o,o1))
    select_Occupation = st.sidebar.selectbox("Occupation",o)
    mapping3 = mapping_Occupation[select_Occupation]

    b = ['Overweight', 'Normal', 'Obese', 'Normal Weight']
    b1 = [3, 0, 2, 1]
    mapping_BMI = dict(zip(b,b1))
    select_BMI = st.sidebar.selectbox("BMI Category",b)
    mapping4 = mapping_BMI[select_BMI]

    sleep_duration = st.sidebar.slider('Hours of Sleep Duration (per day)', min_value= 1, max_value=24)

    quality = st.sidebar.slider('Quality of sleep (scale: 1-10)', min_value=1, max_value=10)

    physical_activity = st.sidebar.slider('Physical Activity Level (minutes/day)')

    stress = st.sidebar.slider('Stress Level (scale: 1-10)', min_value=1, max_value=10)

    heart_rate = st.sidebar.slider('Heart rate (minute)', min_value=60, max_value=170)

    daily_steps = st.sidebar.slider('Number of steps you takes (per day)', max_value=10000)

    systolic = st.sidebar.selectbox("Systolic", [126, 125, 140, 120, 132, 130, 117, 118, 128, 131, 115, 135, 129,
       119, 121, 122, 142, 139])
    diastolic =  st.sidebar.selectbox("Diastolic", [83, 80, 90, 87, 86, 76, 85, 84, 75, 88, 78, 77, 79, 82, 92, 95, 91])

    blood_pressure_classification = classify_blood_pressure(systolic, diastolic)

   
    df_for_view = pd.DataFrame({'Gender':select_gender,
                  'Age':select_age,
                  'Occupation':select_Occupation,
                  'BMI Category':select_BMI,
                  'Sleep Duration':sleep_duration,
                  'Quality of Sleep':quality,
                  'Physical Activity Level':physical_activity,
                  'Stress Level':stress,
                  'Heart Rate':heart_rate,
                  'Daily Steps':daily_steps,
                  'Systolic':systolic,
                  'Diastolic':diastolic
                  }, index=[0])
    
    df_for_pred = pd.DataFrame({'Gender':mapping1,
                  'Age':mapping2,
                  'Occupation':mapping3,
                  'BMI Category':mapping4,
                  'Blood Pressure Classification':blood_pressure_classification,
                  'Sleep Duration':sleep_duration,
                  'Quality of Sleep':quality,
                  'Physical Activity Level':physical_activity,
                  'Stress Level':stress,
                  'Heart Rate':heart_rate,
                  'Daily Steps':daily_steps,
                  'Systolic':systolic,
                  'Diastolic':diastolic
                  }, index=[0])
    
    st.write(df_for_view)
    return df_for_pred




def prediction(df):
    model = pickle.load(open('model\model.pkl','rb'))
    scaler = pickle.load(open('model\scaler.pkl','rb'))

    col1, col2 = st.columns([3, 3])
    
    scaled_input = scaler.transform(df)  # Convert DataFrame to numpy array
    prediction = model.predict(scaled_input)
    with col1:
     if prediction == 2:
        col1.subheader('Normal')
     elif prediction == 1:
        col1.subheader('Sleep Apnea')
     else:
        col1.subheader('Insomnia')
     probs = model.predict_proba(scaled_input)[0]
     st.write("Probability of having Insomnia: ", probs[0])
     st.write("Probability of having Sleep Apnea: ", probs[1])
     st.write("Probability of having Normal Sleep: ", probs[2])

    with col2:
        recommendation(prediction)


def main():
    st.set_page_config(page_title="Sleep Disorder Prediction",
                    page_icon="😴", 
                    layout="wide", 
                    initial_sidebar_state="expanded")
    with st.container():
        st.title('Sleep Disorder Prediction😴')
        st.write('The Sleep Disorder Prediction App is a cutting-edge tool designed to assess and predict the likelihood of sleep disorders in individuals based on various features and parameters. Leveraging advanced machine learning algorithms, the app analyzes input data related to sleep patterns, lifestyle habits, medical history, and demographic information to provide personalized insights and recommendations.')
    
    df_pred = sidebar()
    result = st.button("Click for Result")
    if result:
        prediction(df_pred)
    


  
if __name__ == '__main__':
    main()