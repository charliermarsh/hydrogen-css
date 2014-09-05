Hydrogen-CSS
============

Hydrogen-CSS is a wrapper around [Helium-CSS](https://github.com/geuis/helium-css) that aims to make cleaning up and compressing your stylesheets even easier.

[Helium](https://github.com/geuis/helium-css) is a great tool. It allows you to identify unused CSS selectors on specificed URLs and generate reports detailing useless selectors. But as it stands, Helium has a few drawbacks:

- It must be run from the browser.
- It requires adding extra JavaScript to the target webpage.
- It generates output that must be interpreted and acted upon manually.

Hydrogen aims to automate the *generation* and *interpretation* of these reports through a two-step process:

1. Generate Helium reports from the command-line using [PhantomJS](http://phantomjs.org) for headless browsing.
2. Create new, minified stylesheets based on the feedback contained within these reports.

Note that this tool was developed with no official connection to Helium-CSS.

## How It Works

As mentioned above, Hydrogen uses PhantomJS to avoid the need for running Helium in a browser. Additionally, using PhantomJS, we can inject the JavaScript required by Helium and remove the burden from the user of having to include any additional scripts.

Once a Helium report has been produced, it's sent off to a Python script which handles the parsing of said report. Finally, a new (minified) stylesheet is saved locally using the `[initial_name]-min.css` naming convention.

## Requirements

Hydrogen is built with JavaScript (for generating Helium reports) and Python (for generating new stylesheets). Additionally, you'll need (or want) the following:

- [PhantomJS](http://phantomjs.org)
- [cssutils](https://pypi.python.org/pypi/cssutils/)
- [CoffeeScript](http://coffeescript.org) (optional, as I've included the compiled JavaScript as well)

Note that the `helium.js` file in this repository differs from that in [helium-css](https://github.com/geuis/helium-css).

## Usage

To assess your CSS, you'll need to be running a local server (so as to allow for the injection of JavaScript via PhantomJS). Once that's established, you can run `hydrogen.py` which takes a list of target URLs as command-line arguments.

Your workflow might resemble the following (from the 'hydrogen-css' directory):

```python
python -m SimpleHTTPServer 8000
python hydrogen.py --report 'http://localhost:8000/path/to/page1.html' 'http://localhost:8000/path/to/page2.html'
```

Note that `--report` enables logging of statistics regarding CSS compression. `hydrogen.py` also includes a `--setup` option that will compile the target CoffeeScript files and attempt to download the Python requirements using [PyPI](https://pypi.python.org/pypi/pip).

## Disclaimer

Hydrogen is relatively incomplete and untested—I built it primarily as an experiment. I've seen good results on a couple of relatively simple web pages thus far, but there's a whole world of crazy behavior out there that I haven't had the chance to explore. There are bugs lurking beneath the surface.

With that in mind, feel free to clone, commit, fork, pull—whatever you like. Above all, let me know when you encounter errors and I'll do my best to get back to you.
