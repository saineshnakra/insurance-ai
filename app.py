import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Set the page title and header
st.set_page_config(page_title="Health Friend", page_icon="🧠", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #f4f4f4;
        padding: 20px;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: #003366;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #555;
    }
    .sidebar {
        background-color: #F4F4F4;
    }
    .button-primary {
        background-color: #00AEEF;
        color: white;
    }
    .button-success {
        background-color: #28A745;
        color: white;
    }
    .alert-warning {
        background-color: #FFD700;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Health Friend</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your assistant for insurance-covered services</div>', unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.header("Upload Insurance Policy")
    uploaded_file = st.file_uploader("Upload your insurance policy (PDF format)", type="pdf")
    get_free_stuff = st.button("Get me free stuff!", key="free_stuff_button")

    st.header("Your Location")
    user_location = st.text_input("Where are you located? (City and Zipcode)")
    
    st.header("Select Service")
    user_booking_input = st.text_input("Which service would you like to book?")
    find_service_location = st.button("Where can I get this service?", key="service_location_button")

# Process the uploaded PDF
pdf_text = ""
if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
else:
    st.info("Please upload your insurance policy to proceed.")

# If the "Get me free stuff!" button is pressed and the PDF is uploaded
if get_free_stuff and pdf_text:
    st.markdown("### Preventive and Free Services Covered:")
    with st.spinner('Retrieving services covered by your insurance...'):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an insurance expert."},
                {"role": "user", "content": f"Please list all preventive and free services covered in this insurance policy, along with how they can be accessed. \n\nHere is the insurance policy: {pdf_text}"}
            ],
        )
        services_covered = response.choices[0].message.content.split('\n')
        
        st.success("Here is a list of services covered by your insurance:")
        for service in services_covered:
            st.write(service)

# Display a section for booking the chosen service
if find_service_location and user_booking_input and user_location:
    st.markdown("### Booking Information")
    with st.spinner('Finding booking locations...'):
        booking_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an insurance expert."},
                {"role": "user", "content": f"Where can I book {user_booking_input} near {user_location} according to my insurance: {pdf_text}?"}
            ],
        )
        st.success("You can book this service at the following location(s):")
        st.write(booking_response.choices[0].message.content)

else:
    if user_booking_input or find_service_location:
        st.info("Please specify your location in the sidebar to proceed with booking.")
    else:
        st.info("Please specify a service and your location in the sidebar to proceed with booking.")

# Footer for app information
st.markdown("""
    <hr style='border-top: 1px solid #ccc;'/>
    <div style="text-align:center">
        <small>&copy; 2024 Health Friend | Your assistant for navigating health insurance services</small>
    </div>
""", unsafe_allow_html=True)

# Add styles for interactive elements
def add_custom_css():
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #00AEEF;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 1em;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #007BFF;
    }
    .stTextInput>input {
        border-radius: 4px;
        border: 1px solid #ccc;
        padding: 8px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply custom styles
add_custom_css()