# AI Health & Wellness Coach

An AI-powered health and wellness coaching system using CrewAI that provides personalized guidance across nutrition, fitness, mindfulness, and progress tracking. Built with Streamlit for a beautiful, interactive web interface.

## 🚀 Live Demo

[Deploy to Streamlit Community Cloud](#deployment)

## ✨ Features

- **🥗 Nutritionist Agent**: Creates personalized meal plans based on user goals and dietary preferences
- **💪 Fitness Planner Agent**: Designs effective workouts using available equipment
- **🧘‍♀️ Mindfulness Guide Agent**: Provides meditation and stress management exercises
- **📅 Schedule Coordinator Agent**: Integrates all activities into a cohesive daily schedule
- **📊 Progress Reporter Agent**: Generates weekly health summaries and motivation
- **🎨 Beautiful UI**: Modern, responsive interface with Google-inspired design
- **🤖 Multi-Agent Collaboration**: AI agents work together to create comprehensive health plans

## 🛠️ Local Setup

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-health-coach.git
cd ai-health-coach
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

5. Run the application:
```bash
streamlit run app.py
```

## 🚀 Deployment

### Streamlit Community Cloud

1. **Fork this repository** to your GitHub account

2. **Set up your OpenAI API key**:
   - Go to [Streamlit Community Cloud](https://share.streamlit.io/)
   - Create a new app
   - Connect your GitHub repository
   - Add your OpenAI API key as a secret:
     - Go to your app settings
     - Add secret: `OPENAI_API_KEY` with your actual API key

3. **Deploy**:
   - Streamlit will automatically detect the `streamlit_app.py` file
   - Your app will be available at `https://your-app-name.streamlit.app`

### Environment Variables

For deployment, make sure to set these environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key

## 📁 Project Structure

```
ai-health-coach/
├── app.py                 # Main Streamlit application
├── streamlit_app.py       # Entry point for Streamlit Community Cloud
├── health_advisor.py      # Agent definitions and tasks
├── health_coach.py        # Core health coaching logic
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

## 🎯 Usage

1. **Set Your Profile**: Use the sidebar to configure your health goals, dietary preferences, fitness level, and available equipment
2. **Generate Plan**: Click "Generate My Health Plan" to start the AI collaboration
3. **Review Results**: Explore the three tabs:
   - **Initial Planning**: See individual agent recommendations
   - **Schedule Integration**: View the coordinated daily schedule
   - **Weekly Report**: Get progress insights and recommendations

## 🔧 Configuration

### Health Goals
- Weight Loss
- Muscle Gain
- Stress Reduction
- Better Sleep
- More Energy

### Dietary Preferences
- Balanced
- Vegetarian
- Vegan
- Keto
- Mediterranean

### Fitness Levels
- Beginner
- Intermediate
- Advanced

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [CrewAI](https://github.com/joaomdmoura/crewAI)
- AI capabilities provided by [OpenAI](https://openai.com/)

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub. 