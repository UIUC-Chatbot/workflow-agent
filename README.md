# Workflow Agent
An AI-powered coding assistant designed to streamline and solve complex scientific computational workflows. Leveraging advanced language models and a suite of development tools, it offers an intuitive interface for executing a wide range of tasks, from data analysis to full-stack development.

## Features
- **Intelligent Planning**: Generates step-by-step plans to achieve specified objectives.
- **Execution Environment**: Runs code snippets using shell
- **Integration**: Seamlessly interacts web browsers, and other tools for a comprehensive development experience.
- **Customizable Workflows**: Tailored to specific scientific domains, enhancing productivity and accuracy.

## Getting Started
1. Clone the repository:
   ```
   git clone https://github.com/UIUC-Chatbot/workflow-agent
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file based on the provided `.env.example`.

4. Install Playwright dependencies for browser automation:
   ```
   playwright install
   ```

5. Prepare the `issue.json` file required for running the agent. This file should contain the issue data in JSON format that the agent will process. For the structure of `issue.json`, refer to the [Issue class definition](type/issue.py).

6. Run the agent:
   ```
   python main.py
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report bugs, and suggest enhancements.

## Acknowledgments
Special thanks to the Center for AI Innovation for supporting this project.
