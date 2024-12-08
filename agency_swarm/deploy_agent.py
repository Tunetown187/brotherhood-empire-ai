import argparse
from agency_swarm.agency import Agency
from agency_swarm.agents import Agent
from agency_swarm.tools import BaseTool, FileSearch, CodeInterpreter

def main():
    parser = argparse.ArgumentParser(description='Deploy an Agency Swarm agent')
    parser.add_argument('--name', required=True, help='Name of the agent')
    parser.add_argument('--role', required=True, help='Role of the agent')
    args = parser.parse_args()

    # Initialize the agent with the specified role
    agent = Agent(
        name=args.name,
        role=args.role,
        tools=[BaseTool, FileSearch, CodeInterpreter],
        goals=[
            f"Act as a {args.role} for the Brotherhood Empire",
            "Follow commands and report back results",
            "Maintain security and confidentiality"
        ]
    )

    # Create an agency with the agent
    agency = Agency(
        agents=[agent],
        tools=[BaseTool, FileSearch, CodeInterpreter]
    )

    # Start the agent
    agency.start()

    # Handle stdin commands
    while True:
        try:
            command = input().strip()
            if command.lower() == 'exit':
                break
            
            # Process the command through the agency
            response = agency.handle_command(command)
            print(f"Response from {args.name}: {response}")
            
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
