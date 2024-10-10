import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Set the page title and header
st.set_page_config(page_title="Insurance GPT", page_icon="🧠", layout="wide")

# Enhanced CSS styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Global styles */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f4f8;
    }

    /* Main container */
    .main {
        padding: 0;
        background: linear-gradient(135deg, #e0e7ff 0%, #f0f4f8 100%);
    }

    /* Title styling */
    .title {
        text-align: center;
        font-size: 4em;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 0;
        margin-top: 20px;
        font-family: 'Poppins', sans-serif;
    }

    /* Subtitle styling */
    .subtitle {
        text-align: center;
        font-size: 1.8em;
        color: #16213e;
        margin-bottom: 30px;
    }

    /* Decorative underline for title */
    .title:after {
        content: '';
        display: block;
        width: 60px;
        height: 4px;
        background-color: #00a8cc;
        margin: 20px auto 0;
        border-radius: 2px;
    }

    /* Informative Bar */
    .info-bar {
        background-color: #00a8cc;
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.2em;
        margin: 40px 0;
        box-shadow: 0 8px 15px rgba(0, 168, 204, 0.2);
        transition: transform 0.3s ease;
    }

    .info-bar:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 25px rgba(0, 168, 204, 0.3);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        background-image: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%);
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    }

    /* Sidebar header */
    .sidebar .element-container h2 {
        color: #1a1a2e;
        font-weight: 600;
        margin-top: 30px;
        font-size: 1.5em;
    }

    /* Button styling */
    .stButton>button {
        background-color: #00a8cc;
        color: white;
        border-radius: 30px;
        border: none;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 1em;
        margin-top: 20px;
        transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #007b99;
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 123, 153, 0.2);
    }

    /* Text input styling */
    .stTextInput>div>div>input {
        border-radius: 30px;
        border: 2px solid #ccc;
        padding: 12px 20px;
        width: 100%;
        font-size: 1em;
        margin-top: 10px;
        transition: border-color 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #00a8cc;
        outline: none;
        box-shadow: 0 0 5px rgba(0, 168, 204, 0.2);
    }

    /* File uploader styling */
    .stFileUploader>div>div>div>button {
        background-color: #00a8cc;
        color: white;
        border-radius: 30px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        font-size: 1em;
        margin-top: 10px;
        transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stFileUploader>div>div>div>button:hover {
        background-color: #007b99;
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 123, 153, 0.2);
    }

    /* Success message styling */
    .stAlert.success {
        background-color: #e6fffa;
        color: #1a535c;
        border-left: 5px solid #00a8cc;
        border-radius: 8px;
        padding: 20px;
        font-size: 1em;
    }

    /* Info message styling */
    .stAlert.info {
        background-color: #f0f4f8;
        color: #1a1a2e;
        border-left: 5px solid #00a8cc;
        border-radius: 8px;
        padding: 20px;
        font-size: 1em;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        font-size: 1em;
        color: #777;
        margin-top: 50px;
        padding-bottom: 20px;
        font-family: 'Poppins', sans-serif;
    }

    /* Horizontal rule styling */
    hr {
        border-top: 1px solid #ccc;
        margin-top: 50px;
        margin-bottom: 50px;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f0f4f8;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #00a8cc;
        border-radius: 10px;
        border: 2px solid #f0f4f8;
    }

    /* Responsive design */
    @media only screen and (max-width: 768px) {
        .title {
            font-size: 2.5em;
        }
        .subtitle {
            font-size: 1.2em;
        }
        .info-bar {
            font-size: 1em;
            padding: 15px;
        }
        .stButton>button {
            padding: 12px 25px;
            font-size: 0.9em;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Main title and subtitle
st.markdown('<div class="title">InsuranceGPT</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered assistant for insurance-covered services</div>', unsafe_allow_html=True)

# Informative Bar
st.markdown("""
    <div class="info-bar">
        <strong>Welcome!</strong> Upload your insurance policy to discover covered preventive services and find booking locations near you.
    </div>
""", unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.header("📄 Upload Insurance Policy")
    uploaded_file = st.file_uploader("Upload your insurance policy (PDF format)", type="pdf")
    get_free_stuff = st.button("Get me free stuff!", key="free_stuff_button")

    st.header("📍 Your Location")
    user_location = st.text_input("Where are you located? (City and Zipcode)")

    st.header("🔎 Select Service")
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

# Function to generate responses using OpenAI GPT-4
def generate_response(prompt):
    with st.spinner('Processing...'):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an insurance expert."},
                {"role": "user", "content": prompt}
            ],
        )
    return response.choices[0].message.content

# If the "Get me free stuff!" button is pressed and the PDF is uploaded
if get_free_stuff and pdf_text:
    st.markdown("### 🛡️ Preventive and Free Services Covered:")
    prompt = f"""
    You are an insurance expert. Please list all preventive and free services covered in this insurance policy, along with how they can be accessed.

    Here is the insurance policy:

    {pdf_text}
    """
    services_response = generate_response(prompt)
    services_covered = services_response.strip().split('\n')

    st.success("Here is a list of services covered by your insurance:")
    for service in services_covered:
        st.write(f"- {service.strip()}")

# Display a section for booking the chosen service
if find_service_location and user_booking_input and user_location:
    st.markdown("### 📆 Booking Information")
    prompt = f"""
    You are an insurance expert. Where can I book {user_booking_input} near {user_location} according to my insurance policy?

    Here is the insurance policy:

    {pdf_text}
    """
    booking_response = generate_response(prompt)
    st.success("You can book this service at the following location(s):")
    st.write(booking_response)

elif find_service_location and not user_location:
    st.info("Please specify your location in the sidebar to proceed with booking.")

elif find_service_location and not user_booking_input:
    st.info("Please specify a service in the sidebar to proceed with booking.")

# Footer for app information
st.markdown("""
    <hr/>
    <div class="footer">
        &copy; 2024 <strong>InsuranceGPT</strong> | Your AI assistant for navigating health insurance services
    </div>
""", unsafe_allow_html=True)

# Apply custom styles
def add_custom_css():
    st.markdown("""
    <style>
    /* Additional styling for Streamlit elements */

    /* Adjust the width of the main content area */
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Style Streamlit success and info messages */
    .stAlert {
        background-color: #f0f4f8;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .stAlert.success {
        border-left: 5px solid #00a8cc;
    }

    .stAlert.info {
        border-left: 5px solid #007bff;
    }

    /* Style for headers in main content */
    h3 {
        color: #1a1a2e;
        font-weight: 600;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    /* Style for the spinners */
    .stSpinner > div > div {
        border-top-color: #00a8cc;
        border-left-color: #00a8cc;
    }

    /* Adjust padding and margins for main content */
    .element-container {
        padding: 0;
    }

    /* Code block styling */
    .stCodeBlock {
        background-color: #f0f4f8;
        border-radius: 8px;
    }

    </style>
    """, unsafe_allow_html=True)

add_custom_css()
