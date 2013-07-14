Hydrogen-CSS
============

Hydrogen-CSS is a wrapper around [Helium-CSS](https://github.com/geuis/helium-css) that aims to make cleaning up and compressing your stylesheets even easier.

[Helium](https://github.com/geuis/helium-css) is a great tool. It allows you to identify unused CSS selectors on specificed URLs and generate reports detailing useless selectors. But as it stands, Helium has a few drawbacks: it must be run from the browser, it requires the addition of some extra JavaScript to run, and its reports must be parsed and interpreted by hand.

Hydrogen aims to automate the *generation* and *interpretation* of these reports through a two-step process:
1. Generate Helium reports from the command-line using [PhantomJS](http://phantomjs.org) for headless browsing.
2. Create new, minified stylesheets based on the feedback contained in these reports.

Note that this tool was developed with no official connection to Helium-CSS.

# How It Works

As mentioned above, Hydrogen uses PhantomJS to avoid the need for running Helium in a browser. Additionally, using PhantomJS, we can inject the JavaScript required by Helium and remove the burden from the user of having to include any additional scripts.

Once a Helium report has been produced, it's sent off to a Python script which handles the parsing of said report. Finally, a new (minified) stylesheet is saved locally using the '[initial_name]-min.css' naming convention.

# Requirements

Hydrogen is built with JavaScript (for generating Helium reports) and Python (for generating new stylesheets). Additionally, you'll need (or want) the following:
- [PhantomJS](http://phantomjs.org)
- [cssutils](https://pypi.python.org/pypi/cssutils/)
- [CoffeeScript](http://coffeescript.org) (optional, as I've included the compiled JavaScript)

Note that the 'helium.js' file in this repository differs from that in [helium-css](https://github.com/geuis/helium-css).

# Usage

To assess your CSS, you'll need to be running a local server (so as to allow for the injection of JavaScript via PhantomJS). Once that's established, you can run 'hydrogen.py' which takes a list of target URLs as command-line arguments.

Your workflow might resemble the following (from the 'hydrogen-css' directory):

    python -m SimpleHTTPServer 8000
    python hydrogen.py 'http://localhost:8000/path/to/page1.html' 'http://localhost:8000/path/to/page2.html' --report

Note that the '--report' option enables logging of statistics regarding CSS compression. 'hydrogen.py' also includes a '--setup' option that will compile the target CoffeeScript files and attempt to download the Python requirements using [pip](https://pypi.python.org/pypi/pip).

# Warnings

Hydrogen is in its early stages. Admittedly, it's incomplete (most notably, multi-page support is not available yet). Again, admittedly, it's relatively untested. I've seen good results on a couple of relatively simple web pages thus far, but there's a whole world of crazy web behavior out there that I haven't had the chance to explore. There are bugs lurking beneath the surface.

With that in mind, feel free to clone, commit, fork, pull--whatever you like. Above all, let me know when you encounter errors and I'll do my best to get back to you.

# Contact

You can get in touch with me, [Charlie Marsh](http://www.princeton.edu/~crmarsh), here or on my personal email (crmarsh@princeton.edu).
