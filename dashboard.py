import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to load Excel file and process data
def load_data():
    file_path = 'farmers_data.xlsx'  # Assuming 'data.xlsx' is in the same directory as this script
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        st.sidebar.write("Columns in DataFrame:", df.columns.tolist())
        return df
    except FileNotFoundError:
        st.error("File not found. Please ensure 'farmers_data.xlsx' is in the same directory as this script.")
        return None
    except pd.errors.ParserError as e:
        st.error(f"Error parsing Excel file: {e}")
        return None
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

# Function to display dashboard
def display_dashboard(df):
    st.markdown('<div class="center-content">', unsafe_allow_html=True)

    st.header("📊 Village Farming Analytics")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        st.subheader("👨‍🌾👩‍🌾Farmer Overview🏘️🌾")
        st.markdown("Here you can find an overview of the farmers' data.")
        st.markdown(f"""
            <div class="metric-box bg-lightyellow">
                <h3>👨‍🌾👩‍🌾Total Farmers</h3>
                <p>{df['Farmer ID'].nunique()}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-box bg-lightgreen">
                <h3>🏘️ Total Villages</h3>
                <p>{df['Village'].nunique()}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="metric-box bg-lightblue">
                <h3>🌾 Total Land Holding (Ha)</h3>
                <p>{df['Total Area Holding (Ha)'].sum()}</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("👨‍🌾Farmers Distribution👩‍🌾")
        st.markdown("Distribution of farmers by gender.")
        production_by_gender = df['Gender M/F'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(production_by_gender, labels=production_by_gender.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        ax1.axis('equal')
        st.pyplot(fig1)
        plt.clf()  # Clear plot after displaying to avoid overlapping

    with col3:
        st.subheader("Farmers in Selected Village 🏘️👩‍🌾👨‍🌾")
        st.markdown("Displaying details of farmers in a selected village.")
        selected_village = st.selectbox('Select Village', options=df['Village'].unique())
        village_data = df[df['Village'] == selected_village]
        st.dataframe(village_data[['Farmer ID', 'Name of the Farmer', 'Mobile No', 'Village', 'Total Area Holding (Ha)']])

    with col4:
        st.subheader("🌳 Production of Crop")
        st.markdown("Displaying production statistics by crop.")
        if 'Production area for crop' in df.columns:
            fig2, ax2 = plt.subplots(figsize=(8, 6))  # Adjust figure size for bar chart
            crop_production = df['Production area for crop'].value_counts()
            sns.barplot(x=crop_production.index, y=crop_production.values, palette='viridis', ax=ax2)
            ax2.set_title('Production Area for Crops')
            ax2.set_xlabel('Crop')
            ax2.set_ylabel('Count')
            ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig2)
            plt.clf()  # Clear plot after displaying to avoid overlapping

    st.markdown('</div>', unsafe_allow_html=True)

# Streamlit UI elements
st.set_page_config(page_title="Village Farming Analytics", page_icon="🌾", layout="wide")
local_css("styles.css")  # Load custom CSS

st.sidebar.title("👨‍🌾👩‍🌾 Farmer Data Hub")

# Load data directly from Excel file
df = load_data()

if df is not None:
    display_dashboard(df)

# Suppress PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)
