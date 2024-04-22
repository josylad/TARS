from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import ShellTool
from subprocess import Popen, PIPE
from crewai_tools import tool
import subprocess


@tool("Nettacker")
def nettacker(
    targets: str,
    output_format: str = "html",
    graph: str = None,
    profiles: str = None,
    modules: str = None,
    usernames: str = None,
    passwords: str = None,
    ports: str = None,
    user_agent: str = None,
    parallel_module_scan: int = 1,
    retries: int = 3,
    verbose_mode: int = 0,
    api: bool = False,
    api_port: int = 5000,
) -> str:
    """
    Executes an OWASP Nettacker scan and returns the results.

    Parameters:
    - targets (str): The IP address, hostname, or network to scan, separated by commas.
    - output_format (str, optional): Format of the output file ('txt', 'csv', 'html', 'json'), default is 'html'.
    - graph (str, optional): Specifies the type of graph to generate ('d3_tree_v1_graph', 'd3_tree_v2_graph'), default is None.
    - profiles (str, optional): Predefined set of modules (e.g., 'all', 'vuln', 'cve2021').
    - modules (str, optional): Specific module(s) to run, defaults to None which will use Nettacker's default module settings.
    - usernames (str, optional): List of usernames to use during the scan, separated by commas.
    - passwords (str, optional): List of passwords to use during the scan, separated by commas.
    - ports (str, optional): List of ports to scan, separated by commas.
    - user_agent (str, optional): Specify a user agent for HTTP requests, or use 'random_user_agent'.
    - parallel_module_scan (int, optional): Number of modules to scan in parallel.
    - retries (int, optional): Number of retries for a failed connection attempt.
    - verbose_mode (int, optional): Verbosity level (0-5).
    - api (bool, optional): Flag to start the API service.
    - api_port (int, optional): Port number for the API service if started.

    Returns:
    - str: The results of the Nettacker scan or an error message.
    """

    if not targets:
        raise ValueError("Targets are required for scanning.")

    # Build the command with basic and optional parameters
    base_command = f"python nettacker.py -i {targets} -o results.{output_format} --verbose {verbose_mode}"

    if modules:
        base_command += f" -m {modules}"
    if profiles:
        base_command += f" --profile {profiles}"
    if graph:
        base_command += f" --graph {graph}"
    if usernames:
        base_command += f" -u {usernames}"
    if passwords:
        base_command += f" -p {passwords}"
    if ports:
        base_command += f" -g {ports}"
    if user_agent:
        base_command += f" --user-agent '{user_agent}'"
    if parallel_module_scan != 1:
        base_command += f" -M {parallel_module_scan}"
    if retries != 3:
        base_command += f" --retries {retries}"
    if api:
        base_command += f" --start-api --api-port {api_port}"

    # Execute the command using subprocess
    process = subprocess.Popen(
        base_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        raise Exception(f"Error executing Nettacker: {stderr.decode('utf-8')}")

    return stdout.decode("utf-8")
