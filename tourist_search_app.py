import streamlit as st
import asyncio
from browser_use import Agent, Browser
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime
import os
from browser_use.browser.browser import BrowserConfig, BrowserContextConfig

TOURIST_PROMPTS = {
    "attractions": """
        1. Go to Google.com
        2. Search for 'top tourist attractions in {location}'
        3. Find and extract information about at least 3 popular attractions including:
           - Name and brief description
           - Rating and number of reviews
           - Opening hours
           - Ticket prices
           - Location/address
           - Any seasonal considerations
        4. Look for official website links if available
        5. Format the information in a clear, readable way
    """,
    
    "hotels": """
        1. Go to Google.com
        2. Search for 'best hotels in {location}'
        3. Find and extract information about 3 highly-rated hotels including:
           - Hotel name and category (luxury/mid-range/budget)
           - Current price range
           - Star rating and guest reviews
           - Key amenities
           - Location and proximity to attractions
           - Special offers if any
        4. Include booking website links if available
    """,
    
    "restaurants": """
        1. Go to Google.com
        2. Search for 'best restaurants in {location}'
        3. Find and extract details about 3 popular restaurants including:
           - Restaurant name and cuisine type
           - Price range ($/$$/$$$)
           - Rating and number of reviews
           - Popular dishes and specialties
           - Opening hours
           - Location and contact information
           - Reservation requirements if any
    """,
    
    "transport": """
        1. Go to Google.com
        2. Search for 'public transportation {location} tourist guide'
        3. Extract comprehensive information about:
           - Main types of public transport available
           - Ticket costs and pass options
           - How to get from airport to city center
           - Best transport apps to use
           - Tips for using public transport
           - Any tourist-specific transport cards
           - Safety tips and considerations
    """,
    
    "weather": """
        1. Go to Google.com
        2. Search for 'weather forecast {location}'
        3. Extract detailed weather information including:
           - Current temperature and conditions
           - 3-day weather forecast
           - Best time to visit
           - Seasonal considerations
           - What to pack based on current weather
           - Any weather warnings or advisories
    """,
    
    "custom": """
        Go to Google.com and find detailed tourist information about: {query}
        Extract all relevant details including:
        - Main points of interest
        - Practical information (costs, times, locations)
        - Local tips and recommendations
        - Safety considerations
        - Current conditions or restrictions
    """
}

async def tourist_search(location: str, search_type: str, custom_query: str, api_key: str, headless: bool):
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0.7,
    )
    
    # Get appropriate search task
    if search_type == "custom":
        search_task = TOURIST_PROMPTS[search_type].format(query=custom_query)
    else:
        search_task = TOURIST_PROMPTS[search_type].format(location=location)
    
    # Configure browser
    browser_config = BrowserConfig(
        headless=headless,
        disable_security=True,
    )
    
    # Create browser context config
    context_config = BrowserContextConfig(
        minimum_wait_page_load_time=1.0,
        wait_for_network_idle_page_load_time=2.0,
        maximum_wait_page_load_time=10.0,
        wait_between_actions=1.5,
        browser_window_size={'width': 1920, 'height': 1080},
        highlight_elements=True,
        viewport_expansion=800
    )
    
    # Initialize browser
    browser = Browser(config=browser_config)
    
    try:
        # Initialize the agent
        agent = Agent(
            task=search_task,
            llm=llm,
            browser=browser,
            use_vision=True,
            generate_gif=True,
            message_context="""
                When searching, please:
                - Extract comprehensive and accurate tourist information
                - Include prices, hours, and contact details when available
                - Note any seasonal considerations or special events
                - Include local tips and practical advice
                - Mention any current restrictions or advisories
                - Format information in a clear, organized manner
                - Verify information from multiple sources if possible
                - Include official website links when available
            """
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"tourist_info_{location}_{search_type}_{timestamp}.txt"
        
        # Run the agent
        result = await agent.run(max_steps=15)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Tourist Information Search\n")
            f.write(f"Location: {location}\n")
            f.write(f"Category: {search_type}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if result.is_done():
                search_results = result.final_result()
                f.write(search_results)
                return {
                    "status": "success",
                    "results": search_results,
                    "file": output_file,
                    "location": location,
                    "search_type": search_type
                }
            else:
                error_msg = "Search did not complete successfully"
                f.write(f"{error_msg}\n")
                return {"status": "error", "message": error_msg}
            
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Error Report\n")
            f.write(f"Location: {location}\n")
            f.write(f"Search Type: {search_type}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(error_msg)
        return {"status": "error", "message": error_msg}
    finally:
        if browser:
            await browser.close()

def main():
    st.set_page_config(
        page_title="Tourist Information Assistant",
        page_icon="🌍",
        layout="wide"
    )
    
    st.title("🌍 Tourist Information Assistant")
    st.write("Get comprehensive tourist information for any location!")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("Location", placeholder="Enter city or destination...")
        search_type = st.selectbox(
            "What information do you need?",
            ["attractions", "hotels", "restaurants", "transport", "weather", "custom"],
            help="Select the type of tourist information you need"
        )
        
    with col2:
        api_key = st.text_input("Gemini API Key", type="password", placeholder="Enter your Gemini API key...")
        headless = st.checkbox("Run in Headless Mode", value=True, 
                             help="Run browser in background (faster but you won't see the search process)")
        
    # Custom query input if selected
    custom_query = ""
    if search_type == "custom":
        custom_query = st.text_area(
            "Custom Search Query",
            placeholder="Describe what specific tourist information you're looking for..."
        )
    
    # Search button
    if st.button("🔍 Search", type="primary"):
        if not location:
            st.error("Please enter a location")
            return
        if not api_key:
            st.error("Please enter your Gemini API key")
            return
        if search_type == "custom" and not custom_query:
            st.error("Please enter your custom search query")
            return
        
        with st.spinner(f"Searching for {search_type} information in {location}..."):
            result = asyncio.run(tourist_search(location, search_type, custom_query, api_key, headless))
            
            if result["status"] == "success":
                st.success("Information found successfully!")
                
                # Create tabs for different views
                tab1, tab2 = st.tabs(["📝 Results", "📸 Search Process"])
                
                with tab1:
                    st.subheader(f"Tourist Information for {result['location']}")
                    st.markdown(result["results"])
                    st.download_button(
                        label="📥 Download Results",
                        data=result["results"],
                        file_name=f"tourist_info_{result['location']}_{result['search_type']}.txt",
                        mime="text/plain"
                    )
                
                with tab2:
                    gif_path = "agent_history.gif"
                    if os.path.exists(gif_path):
                        st.image(gif_path, caption="Search Process Recording")
                
                st.info(f"Results saved to: {result['file']}")
            else:
                st.error(f"Search failed: {result['message']}")

if __name__ == "__main__":
    main() 