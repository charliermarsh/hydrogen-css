import subprocess
import argparse
import tempfile
import css

# Parse arguments
parser = argparse.ArgumentParser("Automatically generate and download a Helium-CSS report.")
parser.add_argument('target_url', help='The target URL on which to analyze the CSS.')
parser.add_argument('--install',  action='store_true', help='Install Python requirements and compile CoffeeScript')
parser.add_argument('--report', '-r',  action='store_true', help='Print statistics, including compression ratio')
args = parser.parse_args()

# If necessary, install
if args.install:
    # Get external Python packages
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
    # Compile CoffeeScript
    subprocess.call(['coffee', '-c', '-b', 'js/hydrogen.coffee'])

# Generate temporary file to store report
TEMP_REPORT = tempfile.NamedTemporaryFile()

# Run PhantomJS script and capture output
subprocess.call(['phantomjs', 'js/hydrogen.coffee', args.target_url, TEMP_REPORT.name])
css.parseReport(TEMP_REPORT.name, log_statistics=args.report)
TEMP_REPORT.close()
