 ### Enhanced Interactive Learning Assistant
An AI-driven educational assistant that personalizes learning by accepting user-defined topics and objectives, fetching content from various sources, and generating comprehensive, structured reports tailored to individual learning styles.

# Description
The Enhanced Interactive Learning Assistant is built to streamline personalized education. Users provide a topic and goal, and the system interacts with them to understand preferences and prior knowledge. It gathers content from simulated sources (web, video, academic), processes it, and presents a refined educational report including citations, visual aids, and further recommendations.

#  Features
Accepts topic, goal, interest, and preferred learning format

Gathers and processes content from:

🌐 Web (via Wikipedia API)

📽️ Video (simulated transcript)

# Academic (simulated summary)

Personalized interaction based on:

Learning level (Beginner / Intermediate / Advanced)

Focus areas and preferences

Generates structured reports with:

Learning objectives

Summaries and references

Follow-up question support

(Planned) visual aids and diagrams

# Technology Stack

Layer	Tools/Tech Used
Frontend	Streamlit
Backend	Python 3.x
APIs	Wikipedia API, simulated YouTube & Scholar
Libraries	wikipedia-api, streamlit, googletrans, datetime, random, etc.
⚙️ Installation
#  Prerequisites
Python 3.x

pip (Python package manager)

#  Setup
### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Enhanced-Interactive-Learning-Assistant.git
    cd Enhanced-Interactive-Learning-Assistant
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/MacOS
    venv\Scripts\activate     # For Windows
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    streamlit run learning_assistant_app.py
    ```

---

## System Architecture
The system is built using the following components:
- Streamlit: For the interactive user interface.
- Wikipedia API: For retrieving web content summaries.
- YouTube API (simulated): For fetching video transcripts (simulated in the code).
- Google Scholar API (simulated): For retrieving academic research summaries (simulated in the code).

The application allows users to input topics and learning goals, fetches relevant content from simulated sources, and generates a personalized learning report.

---


#  Personalization & Workflow
User enters topic and learning objectives

System interacts to understand:

Knowledge level

Area of interest

Preferred format

Content is gathered and structured

Final report generated with:

Topic summary

Video & academic content (simulated)

References and further suggestions

Option to refine using follow-up queries

# Sample Input & Output
Sample Input

Topic: Machine Learning

Goal: Understand basics

Focus: Supervised vs Unsupervised

Level: Beginner

Format: Text

Sample Output

Summary explanation of ML

Simulated video transcript

Simulated academic summary

References + suggested resources

#  Architecture
+---------------------------+
|   Streamlit UI           |
+---------------------------+
            |
            v
+---------------------------+
|  User Interaction Handler |
+---------------------------+
            |
            v
+---------------------------+
|  Data Gathering Modules   |
| (Web, Video, Academic)    |
+---------------------------+
            |
            v
+---------------------------+
|  Report Generation Engine |
+---------------------------+
            |
            v
+---------------------------+
|  Display + Refinement     |
+---------------------------+
# Future Enhancements
Real integration with YouTube/Google Scholar APIs

Dynamic visual aids (charts, diagrams)

Multi-user support and real-time collaboration

Save/Export learning reports

Docker support for deployment

# Demo
You can test the app by running it locally. Sample input and screenshots are included in the demo/ directory.
