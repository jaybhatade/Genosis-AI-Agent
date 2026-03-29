import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL", "gemini-1.5-flash")

# --- Company Knowledge Base ---

DEEPMIND_DATA = {
    "company": {
        "name": "Google DeepMind",
        "founded": "2010 (as DeepMind Technologies, London); merged with Google Brain in 2023",
        "headquarters": "6 Pancras Square, London, N1C 4AG, United Kingdom",
        "parent": "Alphabet Inc. (via Google)",
        "mission": "Solve intelligence, then use that to solve everything else.",
        "tagline": "Building AI responsibly for the long-term benefit of humanity.",
        "employees": "~3,000+ researchers, engineers, and staff globally",
        "offices": ["London (HQ)", "Mountain View, CA", "New York", "Paris", "Tel Aviv", "Zurich", "Edmonton", "Montreal"],
    },
    "history": {
        "2010": "Founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in London.",
        "2014": "Acquired by Google for approximately £400 million.",
        "2016": "AlphaGo defeats world Go champion Lee Sedol — a landmark AI moment.",
        "2017": "AlphaZero masters Chess, Shogi, and Go from scratch in 24 hours.",
        "2018": "AlphaFold introduced — begins solving the protein folding problem.",
        "2020": "AlphaFold 2 wins CASP14 with unprecedented accuracy.",
        "2021": "AlphaFold database releases structures for nearly all known human proteins.",
        "2022": "Gato: A generalist AI agent capable of 600+ tasks published.",
        "2023": "Google Brain and DeepMind officially merge to form Google DeepMind.",
        "2024": "Demis Hassabis awarded Nobel Prize in Chemistry for AlphaFold contributions.",
    },
    "key_people": {
        "Demis Hassabis": "CEO & Co-founder — neuroscientist, chess prodigy, game designer, AI pioneer.",
        "Shane Legg": "Chief AGI Scientist & Co-founder — focuses on AGI safety and evaluation.",
        "Koray Kavukcuoglu": "Chief Technology Officer (CTO).",
        "Pushmeet Kohli": "VP of Research, Safety & Responsible AI.",
        "Jeff Dean": "Chief Scientist, Google DeepMind (formerly Google Brain lead).",
    },
    "landmark_research": {
        "AlphaGo / AlphaZero": "Mastered board games using reinforcement learning, defeating world champions.",
        "AlphaFold": "Predicted 3D structures of ~200 million proteins — one of the biggest scientific breakthroughs in decades. Used by 1M+ researchers.",
        "AlphaStar": "Reached Grandmaster level in StarCraft II.",
        "AlphaCode 2": "Performs at ~85th percentile in competitive programming contests.",
        "Gato": "A single generalist transformer model that can play games, caption images, chat, and control robots.",
        "Gemini": "Google DeepMind's flagship multimodal LLM family (Ultra, Pro, Nano).",
        "Lyria": "AI music generation model.",
        "GraphCast": "AI weather forecasting — outperforms traditional models at 10-day global forecasts.",
        "GNoME": "Discovered 2.2 million new crystal structures, accelerating materials science.",
    },
    "research_areas": [
        "Reinforcement Learning (RL)", "Large Language Models (LLMs)", "Multimodal AI",
        "AI Safety & Alignment", "Robotics & Embodied AI", "Computational Biology & Health",
        "Neuroscience-inspired AI", "Scientific Discovery (Climate, Materials, Drug Design)",
        "AI Ethics & Governance",
    ],
    "culture_and_visit_info": {
        "dress_code": "Smart casual. No formal dress required.",
        "visit_duration": "Typical industrial visits last 3–5 hours including lab tours, talks, and Q&A.",
        "highlights": [
            "Research lab walkthroughs",
            "Live demos of AI models (subject to NDA/availability)",
            "Talk by a DeepMind researcher or engineer",
            "AlphaFold and Gemini project showcases",
            "Robotics lab preview (select visits)",
            "Q&A session with team members",
        ],
        "photography": "Generally restricted inside labs. Check with your host.",
        "nda": "Visitors may be asked to sign an NDA depending on areas visited.",
        "parking": "Limited on-site. Nearest tube: King's Cross St. Pancras.",
        "accessibility": "Fully accessible building. Contact the host for specific requirements.",
    },
    "internships_and_careers": {
        "programs": ["Research Scientist Intern", "Student Researcher", "Software Engineering Intern", "AI Residency"],
        "eligibility": "Open to PhD, Masters, and exceptional undergrad students in CS, ML, Maths, Physics, Biology.",
        "apply_at": "https://deepmind.google/about/jobs/",
        "tips": "Strong publication record, open-source contributions, or competitive programming results are valued.",
    },
    "social_impact": {
        "AlphaFold for science": "Freely released globally — accelerating drug discovery and rare disease research.",
        "Climate": "GraphCast used by ECMWF; working on fusion energy with UKAEA.",
        "Health": "AI for eye disease detection, breast cancer screening, and ICU deterioration prediction.",
        "Education": "DeepMind Scholarships support underrepresented groups in AI/ML.",
    },
    "faqs": {
        "Is DeepMind part of Google?": "Yes. Since 2023, DeepMind and Google Brain merged into 'Google DeepMind' under Alphabet Inc.",
        "What language is most code written in?": "Python for research; C++ and JAX for performance-critical work.",
        "Does DeepMind publish research openly?": "Yes — at NeurIPS, ICML, ICLR, Nature, and arXiv.",
        "What is AGI?": "Artificial General Intelligence — AI that can perform any intellectual task a human can. DeepMind's long-term goal.",
        "What is JAX?": "A high-performance ML framework by Google, widely used at DeepMind.",
    }
}

# --- State Management Tool ---

def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    """Saves the visitor's query to state. Skips if already saved to prevent re-triggering."""
    # ✅ FIX #1: Guard against re-saving the same prompt in a loop
    if tool_context.state.get("PROMPT") == prompt:
        logging.info("[State] PROMPT unchanged, skipping re-save.")
        return {"status": "skipped"}
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] PROMPT saved: {prompt}")
    return {"status": "success"}

# --- External Tools ---

wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# --- Sub-Agents ---

# 1. Researcher Agent
deepmind_researcher = Agent(
    name="deepmind_researcher",
    model=model_name,
    description="Looks up the visitor's query from DeepMind internal data and Wikipedia if needed.",
    instruction=f"""
    You are a concise research assistant for the Google DeepMind Industrial Visit Guide.

    Internal knowledge base:
    {DEEPMIND_DATA}

    Instructions:
    - Read the visitor's PROMPT below.
    - Pull only the directly relevant facts from the knowledge base above.
    - Only use Wikipedia if the topic is NOT covered in the knowledge base.
    - Output a SHORT bullet-point brief (max 5 points). No paragraphs. No filler.

    PROMPT:
    {{PROMPT}}
    """,
    # ✅ FIX #2: Was {{ PROMPT }} (escaped) — corrected to {PROMPT} for ADK state injection
    tools=[wikipedia_tool],
    output_key="research_data"
)

# 2. Response Formatter Agent
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Turns research notes into a short, friendly, conversational reply.",
    instruction="""
    You are 'Genosis', the Google DeepMind industrial visit guide.

    Your job is to reply to the visitor using the RESEARCH_DATA below.

    STRICT RULES — follow these exactly:
    - Keep the reply under 80 words total.
    - Be conversational and warm, like a knowledgeable friend — NOT a formal report.
    - Use at most 3 bullet points if listing things; otherwise just 1–2 sentences.
    - NO long intros. NO sign-offs longer than 5 words. NO repeating the question back.
    - End with ONE short follow-up question to keep the conversation going.

    RESEARCH_DATA:
    {research_data}
    """
    # ✅ FIX #3: Added strict brevity rules to prevent essay-style responses
)

# --- Workflow Setup ---

deepmind_visit_workflow = SequentialAgent(
    name="deepmind_visit_workflow",
    description="Handles a single visitor question: research → format → reply.",
    sub_agents=[
        deepmind_researcher,
        response_formatter,
    ]
)

# --- Root Agent ---

root_agent = Agent(
    name="Genosis",
    model=model_name,
    description="Entry point for the Google DeepMind Industrial Visit Guide.",
    instruction="""
    You are 'Genosis', the Google DeepMind visit guide.

    RULES — follow strictly to avoid loops:
    1. On the FIRST message only: greet the visitor in 1–2 sentences and ask what they'd like to know.
    2. When the visitor asks a question:
       a. Call 'add_prompt_to_state' ONCE with their question.
       b. Immediately transfer to 'deepmind_visit_workflow'. Do NOT respond yourself.
       c. Do NOT call 'add_prompt_to_state' again until the visitor sends a NEW question.
    3. After the workflow replies, wait for the visitor's next message. Do NOT re-trigger the workflow.
    4. Never repeat a greeting. Never re-save a prompt you already saved.
    """,
    # ✅ FIX #1 (cont): Explicit "call once, wait" instruction prevents the root→workflow→root loop
    tools=[add_prompt_to_state],
    sub_agents=[deepmind_visit_workflow]
)