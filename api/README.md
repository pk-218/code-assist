# CodeAssist API

## Setup

1. Install [Poetry](https://python-poetry.org/docs/)

2. Install the dependencies of the project

   ```bash
   poetry install
   ```

3. Switch on the virtual environment

   ```bash
   poetry shell
   ```

4. Configure the Python virtual environment path in your IDE/code editor. In VS Code, open a `.py` of the project - look at the gutter (bottom-right corner) for Python - click on it - change the interpreter path to the virtual environment Poetry has created for you. To get the interpreter path -

   ```bash
   poetry env info
   ```

5. Run the API
   ```bash
   uvicorn main:app --reload
   ```
