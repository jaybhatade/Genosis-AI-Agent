# Genosis - Google DeepMind Industrial Visit Guide 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK%201.14.0-4285F4)](https://github.com/google/adk)

An intelligent AI agent powered by Google's Agent Development Kit (ADK) that serves as a knowledgeable guide for Google DeepMind industrial visits. Genosis provides instant, conversational answers about DeepMind's history, research, culture, and visiting procedures.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Demo](#demo)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🌟 Overview

Genosis is an AI-powered conversational agent designed to assist visitors planning or attending industrial visits to Google DeepMind. It combines:

- **Internal Knowledge Base**: Comprehensive information about DeepMind's history, research, people, and facilities
- **External Research**: Wikipedia integration for topics beyond the internal database
- **Multi-Agent Architecture**: Specialized sub-agents for research and response formatting
- **Conversational Interface**: Natural, friendly dialogue that keeps responses concise and engaging

## ✨ Features

- 🎯 **Intelligent Question Handling**: Understands and responds to queries about DeepMind's research, culture, and logistics
- 📚 **Rich Knowledge Base**: Covers landmark projects (AlphaGo, AlphaFold, Gemini), key people, research areas, and visit information
- 🔍 **Hybrid Search**: Falls back to Wikipedia for topics not in the internal database
- 💬 **Conversational Design**: Keeps responses under 80 words with natural, engaging tone
- 🔄 **Sequential Processing**: Research → Format → Respond pipeline for consistent quality
- 📊 **State Management**: Tracks conversation context to avoid redundant processing
- ☁️ **Cloud Logging**: Integrated with Google Cloud Logging for monitoring and debugging

## 🏗️ Architecture

Genosis uses a **multi-agent architecture** built on Google ADK:

```
Root Agent (Genosis)
    ├── Tool: add_prompt_to_state
    └── Sub-Agent: deepmind_visit_workflow
            ├── deepmind_researcher (with Wikipedia tool)
            └── response_formatter
```

### Agent Breakdown

1. **Root Agent (Genosis)**: Entry point, handles greetings and routes queries
2. **DeepMind Researcher**: Searches internal knowledge base and Wikipedia
3. **Response Formatter**: Converts research into concise, conversational replies

## 📦 Prerequisites

- **Python**: 3.8 or higher
- **Google Cloud Project**: With ADK enabled
- **Google Cloud Credentials**: Properly configured authentication
- **Dependencies**: Listed in `requirements.txt`

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jaybhatade/genosis-ai-agent.git
cd genosis-ai-agent
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Google Cloud

```bash
# Install Google Cloud SDK (if not already installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate with Google Cloud
gcloud auth application-default login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# .env file

# Model Configuration
MODEL=gemini-1.5-flash

# Optional: Specify alternative models
# MODEL=gemini-1.5-pro
# MODEL=gemini-1.0-pro

# Google Cloud Project (if not set via gcloud)
GOOGLE_CLOUD_PROJECT=your-project-id

# Optional: Logging level
LOG_LEVEL=INFO
```

### Model Options

Genosis supports various Gemini models:
- `gemini-1.5-flash` (default) - Fast, efficient responses
- `gemini-1.5-pro` - More detailed, nuanced responses
- `gemini-1.0-pro` - Stable, production-ready model

## 💻 Usage

### Basic Usage

```python
from agent import root_agent

# Initialize the agent
agent = root_agent

# Start a conversation
response = agent.run("What is AlphaFold and why is it important?")
print(response)
```

### Running as a Script

```python
# example_usage.py
from agent import root_agent

def chat():
    print("Genosis: Hi! I'm your Google DeepMind visit guide. What would you like to know?")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Genosis: Safe travels! Feel free to reach out anytime.")
            break
        
        response = root_agent.run(user_input)
        print(f"Genosis: {response}")

if __name__ == "__main__":
    chat()
```

### Example Queries

Here are some questions Genosis can answer:

- "What should I wear to the DeepMind office?"
- "Tell me about AlphaFold"
- "Who founded DeepMind?"
- "What are the parking options near the London office?"
- "Does DeepMind offer internships?"
- "What is Gemini?"
- "How long does a typical visit last?"

## 🔍 How It Works

### Conversation Flow

1. **User sends a query** → "What is AlphaGo?"
2. **Root agent** saves the query to state via `add_prompt_to_state`
3. **Workflow triggers** the sequential pipeline:
   - **Researcher agent** searches the internal knowledge base
   - If needed, queries Wikipedia for additional context
   - Returns bullet-pointed research data
4. **Formatter agent** converts research into a conversational response
5. **User receives** a concise, friendly answer with a follow-up question

### Knowledge Base Structure

The internal database (`DEEPMIND_DATA`) includes:
- Company information and history
- Key people and leadership
- Landmark research projects
- Research areas and focus
- Visit logistics and culture
- Internship and career information
- Social impact initiatives
- FAQs

### State Management

The agent uses a stateful approach to avoid redundant processing:
- Tracks the current prompt
- Prevents re-saving identical queries
- Maintains conversation context

## 🎬 Demo

### Sample Conversation

```
Genosis: Hi! I'm your Google DeepMind visit guide. What would you like to know?

You: What is AlphaFold?

Genosis: AlphaFold is DeepMind's breakthrough AI system that predicts 3D protein 
structures with unprecedented accuracy. It won CASP14 in 2020 and has since 
released structures for ~200 million proteins, used by 1M+ researchers worldwide. 
Demis Hassabis even won the 2024 Nobel Prize in Chemistry for it! 

Want to know more about DeepMind's other landmark projects?

You: What should I wear to visit?

Genosis: Smart casual works perfectly - no formal dress required! The vibe is 
relaxed but professional. Comfortable shoes are a good idea if you'll be touring 
labs. 

Curious about what the visit includes?
```

### Screenshots

*Coming soon - add screenshots of your deployed agent in action!*

## 📁 Project Structure

```
genosis-ai-agent/
├── agent.py              # Main agent logic and configuration
├── __init__.py           # Package initialization
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md            # This file
└── examples/            # (Optional) Usage examples
    └── chat_example.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit with clear messages**
   ```bash
   git commit -m "Add: New feature description"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Contribution Guidelines

- **Code Style**: Follow PEP 8 guidelines
- **Documentation**: Update README for new features
- **Testing**: Add tests for new functionality
- **Commits**: Use clear, descriptive commit messages
- **Issues**: Check existing issues before creating new ones

### Areas for Contribution

- 🐛 Bug fixes and error handling improvements
- 📝 Expanding the knowledge base
- 🌐 Multi-language support
- 🎨 UI/UX for web deployment
- 📊 Analytics and usage tracking
- 🧪 Unit tests and integration tests
- 📚 Additional documentation and examples

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'google.adk'`
```bash
# Solution: Ensure dependencies are installed
pip install -r requirements.txt
```

**Issue**: Authentication errors
```bash
# Solution: Re-authenticate with Google Cloud
gcloud auth application-default login
```

**Issue**: Agent enters infinite loop
```bash
# Solution: This has been fixed in the current version via state guards
# Ensure you're using the latest code
```

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Jay Bhatade

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Contact

**Jay Bhatade**

- GitHub: [@jaybhatade](https://github.com/jaybhatade)
- Email: [your.email@example.com](mailto:jaybhatade7@gmail.com)
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/jaybhatade)

### Project Links

- **Repository**: [https://github.com/jaybhatade/genosis-ai-agent](https://github.com/jaybhatade/genosis-ai-agent)
- **Issues**: [Report a bug or request a feature](https://github.com/jaybhatade/genosis-ai-agent/issues)
- **Discussions**: [Join the conversation](https://github.com/jaybhatade/genosis-ai-agent/discussions)

---

## 🙏 Acknowledgments

- **Google DeepMind** for the inspiration and knowledge base content
- **Google ADK Team** for the excellent agent development framework
- **LangChain Community** for the Wikipedia integration tool
- All contributors who help improve Genosis

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ by [Jay Bhatade](https://github.com/jaybhatade)

</div>
