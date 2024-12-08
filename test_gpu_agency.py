from agency_swarm import Agency, Agent
from agency_swarm.util.gpu_utils import get_device
from agency_swarm.util.oai import set_openai_key

# You need to replace this with your actual OpenAI API key
OPENAI_API_KEY = "sk-proj-qSCGSUL1ITnbxtVUjZnxT3BlbkFJStsNsz0y0mzofOzONFAW"
set_openai_key(OPENAI_API_KEY)

# Test GPU availability
device = get_device()
print(f"Using device: {device}")

# Define a simple agent
class ResearchAgent(Agent):
    name = "Research Agent"
    description = "A research agent with GPU acceleration"
    instructions = "You are a research agent that helps with information gathering and analysis."
    tools = []
    model = "gpt-4"

# Create agency with GPU support
agency = Agency(
    agency_chart=[
        ResearchAgent()  # Create an instance of the agent
    ],
    use_gpu=True
)

# Test message processing
response = agency.get_completion("Analyze this text and summarize it: " * 1000)  # Create a large input to test GPU
print("Response received:", response[:100] + "...")
