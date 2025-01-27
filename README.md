# Tourist Information Assistant 🌍

A Streamlit-based web application that uses Google's Gemini AI and browser automation to gather comprehensive tourist information for any location. Built using [browser-use](https://github.com/browser-use/browser-use) for browser automation and control.

![Tourist Information Assistant Demo](demo.gif)

## Features

- 🏨 Search for hotels with pricing and amenities
- 🏛️ Find tourist attractions with details and ticket prices
- 🍽️ Discover restaurants with cuisine types and reviews
- 🚌 Get transportation information and tips
- 🌤️ Check weather conditions and forecasts
- 🎯 Custom search for specific tourist information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kanwar19031/Travel-Agent
cd Travel-Agent
```

2. Create and activate a virtual environment:
```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Configuration

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. (Optional) Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run tourist_search_app.py
```

2. Open your browser and go to `http://localhost:8501`

3. Enter:
   - Your destination
   - Type of information needed
   - Gemini API key (if not in .env)
   - Choose headless mode preference

4. Click "Search" and wait for results

## Project Structure

```
tourist-information-assistant/
├── tourist_search_app.py    # Main Streamlit application
├── requirements.txt         # Project dependencies
├── README.md               # Project documentation
└── .env                    # Environment variables (optional)
```

## Dependencies

- browser-use
- streamlit
- langchain-google-genai
- python-dotenv
- asyncio

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

This project uses the [browser-use](https://github.com/browser-use/browser-use) library for browser automation. If you use this project in your research or work, please cite both this project and browser-use:

```bibtex
@software{browser_use2024,
  author = {Müller, Magnus and Žunič, Gregor},
  title = {Browser Use: Enable AI to control your browser},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/browser-use/browser-use}
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Troubleshooting

1. **Browser Issues**:
   - Make sure Playwright is installed correctly
   - Try running in non-headless mode for debugging
   - Check if you have sufficient system resources

2. **API Issues**:
   - Verify your Gemini API key is correct
   - Check your internet connection
   - Ensure you're not exceeding API rate limits

3. **Common Errors**:
   - "No module named 'browser_use'": Run `pip install browser-use`
   - Playwright errors: Run `playwright install` again
   - Memory issues: Close other applications or increase available memory

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/tourist-information-assistant/issues) section
2. Create a new issue with detailed information about your problem
3. Join the [browser-use Discord](https://link.browser-use.com/discord) for community support 
