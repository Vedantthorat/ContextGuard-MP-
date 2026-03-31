from crewai import Agent, Task, Crew
from ai_agent import get_ai_fix

def run_agents(issue):
    
    # 🧠 Analyst Agent
    analyst = Agent(
        role="Cloud Security Analyst",
        goal="Explain cloud security risks clearly",
        backstory="Expert in AWS and cloud vulnerabilities"
    )

    # 🔧 Fix Agent
    fixer = Agent(
        role="DevSecOps Engineer",
        goal="Provide Terraform fixes",
        backstory="Expert in fixing cloud misconfigurations"
    )

    # ⚙️ DevOps Agent
    devops = Agent(
        role="DevOps Engineer",
        goal="Decide whether to block deployment",
        backstory="CI/CD pipeline expert"
    )

    # 📌 Tasks
    analysis_task = Task(
        description=f"Explain this issue: {issue['title']}",
        agent=analyst
    )

    fix_task = Task(
        description=f"Give fix for: {issue['title']}",
        agent=fixer
    )

    decision_task = Task(
        description=f"Should deployment be blocked for severity {issue['severity']}?",
        agent=devops
    )

    # 🚀 Crew Execution
    crew = Crew(
        agents=[analyst, fixer, devops],
        tasks=[analysis_task, fix_task, decision_task]
    )

    result = crew.kickoff()

    return result