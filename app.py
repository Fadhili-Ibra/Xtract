import streamlit as st
from streamlit_option_menu import option_menu
import Home
import ImageUpload
import DocumentScan
import PDFUpload
import login  # Import the login module

# Set page configuration once at the top of the main script
st.set_page_config(
    page_title="Xtract",
    layout="wide"
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        # Initialize session state for login
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        # Show login page if not logged in
        if not st.session_state.logged_in:
            login.main()
            return

        # Show logout button in sidebar
        with st.sidebar:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.experimental_rerun()  # Reload to show login page

            selected_page = option_menu(
                menu_title="Xtract",
                options=['Home', 'Upload Images', 'Scan Documents', 'Upload PDFs'],
                icons=['house-fill', 'image', 'file-earmark-text', 'file-earmark-pdf'],
                menu_icon='menu-button-wide',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "#333"},
                    "icon": {"color": "white", "font-size": "13px"}, 
                    "nav-link": {"color": "white", "font-size": "13px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Display the selected page's content
        if selected_page == 'Home':
            Home.main()
        elif selected_page == 'Upload Images':
            ImageUpload.main()
        elif selected_page == 'Scan Documents':
            DocumentScan.main()
        elif selected_page == 'Upload PDFs':
            PDFUpload.main()

if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()
