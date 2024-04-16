# Code interpretor tools
import io
import time
import uuid
from typing import Any, Optional, Tuple

import termcolor
from e2b import CodeInterpreter, EnvVars, Sandbox, ProcessMessage
from e2b.api.v1.client.exceptions import ForbiddenException


class E2B_class():
  """
  Main entrypoints:
  1. run_python_code(code)
  2. run_r_code(code)
  3. run_shell(shell_command)
  """

  def __init__(self, langsmith_run_id: str, env_vars: Optional[EnvVars] = None):
    """
    # TODOs:
    1. Maybe `git clone` the repo to a temp folder and run the code there
    2. On agent finish, delete sandbox
    """

    self.langsmith_run_id = langsmith_run_id
    try:
      self.sandbox = Sandbox(env_vars=env_vars)
    except ForbiddenException as e:
      print(
          termcolor.colored(
              "You have reached the maximum number of concurrent E2B sandboxes. Please close some sandboxes before creating new ones.",
              'red',
              attrs=['bold']))
      print(termcolor.colored(f"Error: {e.body}", 'red'))
      exit()

    self.sandboxID = self.sandbox.id
    # self.sandbox.keep_alive(2 * 60)  # 2 minutes for now.
    # self.sandbox.keep_alive(60 * 60 * 1)  # 1 hour max
    self.command_timeout = 3 * 60  # 3 minutes
    self.existing_files = []
    self.working_dir = '/home/user/'
    self.curr_terminal_output = ''
    self.install_base_packages()

  def __del__(self):
    try:
      self.sandbox.close()
    except Exception:
      print("Failed to close e2b sandbox, probably fine.")

  def install_base_packages(self):
    self.install_r_packages()

  def install_python_packages(self):
    self.run_shell("pip install -U numpy pandas matplotlib seaborn scikit-learn scipy")

  def install_r_packages(self):
    self.run_shell("sudo apt-get install r-base r-base-dev -y")

  def run_python_code(self, code: str):
    print(termcolor.colored("RUNNING PYTHON CODE:", 'blue', attrs=['bold', 'underline']))
    print(termcolor.colored(code, 'blue'))

    code_file = io.StringIO(code)
    fileid = str(uuid.uuid4())
    code_file.name = fileid + ".py"
    filepath = self.sandbox.upload_file(code_file)
    shell_output = self.run_shell(f"python {filepath}")
    return shell_output

  def run_r_code(self, code: str):
    print(termcolor.colored("RUNNING R CODE:", 'green', attrs=['bold', 'underline']))
    print(termcolor.colored(code, 'green'))

    code_file = io.StringIO(code)
    fileid = str(uuid.uuid4())
    code_file.name = fileid + ".r"
    filepath = self.sandbox.upload_file(code_file)
    shell_output = self.run_shell(f"Rscript {filepath}")
    return shell_output

  def run_shell(self, shell_command: str):
    print(termcolor.colored(f"SHELL EXECUTION with command: {shell_command}", 'yellow', attrs=['bold']))
    self.curr_terminal_output = ''

    start_time = time.monotonic()
    # self.exit_event = threading.Event()
    proc = self.sandbox.process.start(
        cmd=shell_command,
        on_stdout=self.handle_terminal_on_data,
        on_stderr=self.handle_terminal_on_error,
        # on_exit=on_exit,
        cwd=self.working_dir)

    proc.wait()

    print(
        termcolor.colored(f"$ Shell execution complete, Runtime: {(time.monotonic() - start_time):.2f} seconds",
                          'yellow',
                          attrs=['bold']))
    return self.curr_terminal_output

  def handle_terminal_on_data(self, message: ProcessMessage):
    data = str(message)
    self.curr_terminal_output += str(data)
    print(termcolor.colored(data, 'yellow'))

  def handle_terminal_on_error(self, message: ProcessMessage):
    data = str(message)
    self.curr_terminal_output += str(data)
    print(termcolor.colored("Error in E2B Sandbox:", 'red', attrs=['bold']))
    print(termcolor.colored(data, 'red', attrs=['bold']))



if __name__ == "__main__":
    # Example usage
    langsmith_run_id = str(uuid.uuid4())
    e2b = E2B_class(langsmith_run_id=langsmith_run_id)
    code = """sayHello <- function(){
print('hello')
}

sayHello()

    """
    print(e2b.run_python_code("print('Hello World')"))
    print(e2b.run_r_code(code))
    print(e2b.run_shell("ls -la"))
    del e2b
    print("Sandbox closed.")
