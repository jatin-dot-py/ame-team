# AI Matrix Engine
## ame-team Project

### Bridging the gap between current AI capabilities and real-world business needs
AI has become ubiquitous and highly anticipated across various sectors. Yet, when businesses attempt to integrate AI into practical applications, they often find its output falls short of replacing human tasks. AI Matrix Engine uses groundbreaking technology and a novel approach that bridges this gap. By orchestrating an array of AI models, it not only combines and customizes outputs but also elevates them to unprecedented levels of quality and relevance. The result? Solutions that not only meet but surpass business expectations, enabling seamless automation of tasks traditionally performed by humans—all with remarkable simplicity and no coding required. This isn't just an enhancement of AI capabilities; it's a redefinition of what's possible, setting a new standard for AI in practical applications, along with the capability to dynamically adapt to next generations of AI Models.

## Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.12**: This project requires Python 3.12. Check your Python version by running `python --version` in your terminal. If you do not have Python 3.12, you can download it from [python.org](https://www.python.org/downloads/).
- **Poetry for Dependency Management**: This project uses Poetry to manage dependencies. If you're not familiar with Poetry, it is crucial that you install it and learn the basics. Install Poetry by following the instructions on [Poetry's official site](https://python-poetry.org/docs/).

### Installing Poetry
If you do not have Poetry installed, you can install it with the following command:

```bash
curl -sSL https://install.python-poetry.org | python -
```

Or, for Windows, use PowerShell:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Configuring the Project
After installing Poetry, navigate to the project's root directory and run the following command to install all dependencies specified in `pyproject.toml`:

```bash
poetry install
```

This command will create a virtual environment and install all the necessary dependencies to ensure you have a consistent development environment.

Please make sure to configure these tools on your local development environment before proceeding with any code contributions.

This repository serves as a place for each team member to work on their given projects, prior to having them added to the main project.

## Important steps:
1. Utilize Poetry for dependency management to stay consistent with the main project.
2. Confirm all new packages with Armani to ensure no conflicts with the main project.
3. Write clean code that follows the basic guidelines we have in place:
   - Keep functions and methods small and modular.
   - Create documentation for each script that explains the purpose, the various things involved, and most importantly, be detailed about the “entry” into the script.
4. Use simple and clean docstrings that tell a human reader what the function does. (It's best to write docstrings when you are done with a script so you do not accidentally leave outdated information.
5. Be careful that you do not change or move files that are in various places, such as "common" or other places that may not make sense when looking only at this code. (They serve a purpose in the bigger project)
6. If you can see room for improvement in any of the helper or utility directories, please inform Armani to make sure you have the full context and then you can proceed with your improvements.
7. While this project is not set up as a Django project, the main project is built on Django, so in some places, you may see code that is designed to mimic Django, without involving it.
   - If you see dependencies on Django, you can comment them out and create a local equivalent for it.
8. It's very important that any changes to directory structure, filenames, and function, class or method signatures are cleared through Armani to avoid potential conflicts.

Thank you for being a part of this incredible project!

## CI/CD:
This is a core concept that MUST be adhered to by everyone!
- You must push your latest code to git daily.
- Each day, you must start by getting the latest version of Main and merging it with your local code to ensure you do not "fall behind" and then cause major conflicts later or have errors by other developers go unnoticed.
- If you have things that are broken or untested, push them to a new branch, until you get them fixed. You still must push everything daily.
- Each day, if your code does not cause conflicts, it's important that we push it to the main, even if you are not done yet, as long as there are no major bugs in your code that hurt the overall project.


## Sample Usage:
Include a sample usage section at the bottom of each script to demonstrate how it can be run. This should show the main entry point and usage examples. You may include multiple examples and comment out those that are less crucial, but ensure that the primary example is ready to execute with appropriate sample arguments.

```python
if __name__ == "__main__":
    # Example usage
    sample_data = get_sample_data(app_name="automation_matrix", data_name="markdown_content", sub_app="ama_ai_output_samples")
    print(sample_data)
```

This snippet demonstrates how to execute a typical script within this project by fetching and displaying some sample data. This approach helps new contributors understand how to interact with the scripts and test them independently.

Thank you for following these guidelines, which are designed to help all of us.
