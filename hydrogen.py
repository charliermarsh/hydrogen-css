import subprocess
import argparse
import tempfile
import css


def runHydrogen(targetURLs, REPORT=False, SETUP=False):
    # check if arg is list of URLs or single URL
    if type(targetURLs) is list:
        targetURLs = '\n'.join(targetURLs)

    # If necessary, setup
    if SETUP:
        # Get external Python packages
        subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
        # Compile CoffeeScript
        subprocess.call(['coffee', '-c', '-b', 'js/automate.coffee'])

    # Generate temporary file to store report
    TEMP_REPORT = tempfile.NamedTemporaryFile()

    # Run PhantomJS script and capture output
    subprocess.call(['phantomjs', 'js/hydrogen.coffee', targetURLs, '-w', TEMP_REPORT.name])
    css.parseReport(TEMP_REPORT.name, log_statistics=REPORT)
    TEMP_REPORT.close()

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser('Automatically generate and download a Helium-CSS report.')
    parser.add_argument(
        'target_urls', nargs='+', help='The target URLs on which to analyze the CSS.')
    parser.add_argument('--setup', '-s', action='store_true',
                        help='Install Python requirements and compile CoffeeScript')
    parser.add_argument(
        '--report', '-r', action='store_true', help='Print statistics, including compression ratio')
    args = parser.parse_args()
    runHydrogen(args.target_urls, REPORT=args.report, SETUP=args.setup)
