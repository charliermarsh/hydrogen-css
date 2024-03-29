import cssutils
import logging
import re
import os

# Disable logging
cssutils.log.setLevel(logging.FATAL)

# Definitions
STYLE_RULE = 1


def toStylesheet(filename):
    if os.path.exists(filename):
        return cssutils.parseFile(filename)
    return cssutils.parseUrl(filename)


def saveStyleSheetAs(sheet, filename):
    f = open(filename, "wb")
    f.write(sheet.cssText)


def saveMinifiedStylesheetAs(sheet, filename):
    cssutils.ser.prefs.useMinified()
    saveStyleSheetAs(sheet, filename)
    cssutils.ser.prefs.useDefaults()


def cleanSheetForStylesheet(originalName):
    return originalName.split('/')[-1].replace('.css', '-clean.css')


def cleanCSS(report):
    # convert to cssutils stylesheet objects
    cssFilename, rules = report
    sheet = toStylesheet(cssFilename)
    # create identical copy for output
    cleanSheet = toStylesheet(cssFilename)

    # used to divide rules in stylesheets
    divider = re.compile(r'(.*) {')

    # need to track indices
    offset = 0
    for i in range(len(sheet.cssRules)):
        rule = sheet.cssRules[i]
        if not rule.type == STYLE_RULE or not rule.cssText:
            continue

        # get list of names for ith CSS rule
        m = divider.search(rule.cssText)
        names = m.group(1)

        # if there is an item from the Helium report matching this collection of names...
        if names in rules:
            # aggregate all non-green terms
            newSelector = ""
            # pair each name with its type (e.g., {G})
            for s, c in zip(names.split(', '), rules[names]):
                # only add to list of used selectors if type isn't {G}
                if not c == 'G':
                    if newSelector:
                        newSelector += ", "
                    newSelector += s
            # if any selectors remaining, must keep rule
            if not newSelector:
                cleanSheet.deleteRule(i - offset)
                offset += 1
            else:
                cleanSheet.cssRules[i - offset].selectorText = newSelector
    return cleanSheet


def logStatistics(initialSheet, finalSheet):
    # Report number of rules removed
    diff = len(initialSheet.cssRules) - len(finalSheet.cssRules)
    # Save final sheet to temp file
    saveMinifiedStylesheetAs(finalSheet, 'temp_final')
    final_size = os.path.getsize('temp_final')
    # Report compression ratio
    saveStyleSheetAs(initialSheet, 'temp')
    compression_ratio = 100.0 * os.path.getsize('temp') / final_size
    # Report compression ratio over minified initial
    saveMinifiedStylesheetAs(initialSheet, 'temp_min')
    compression_ratio_min = 100.0 * os.path.getsize('temp_min') / final_size
    # Remove temp files
    os.remove('temp')
    os.remove('temp_min')
    os.remove('temp_final')
    print 'Output file: %d bytes.\nRemoved %d rules.\nSaved %.2f%% over original.\nSaved %.2f%% over minified original.' % (final_size, diff, compression_ratio, compression_ratio_min)


def parseReport(report_filename, log_statistics=False):
    """Parse a report generated by Helium and produce 'clean' versions of each named stylesheet.

    Keyword arguments:
    report_filename -- the name of the report file generated by Helium

    """
    def parseRule(rule):
        # we convert [{Type}name] into ([Type], "name1, name2, ...")
        def matchSelector(selector):
            return re.match(r'\{(.+)\}(.+)', selector)
        matches = [matchSelector(s) for s in rule]
        matches = [m for m in matches if m]
        types = [m.group(1) for m in matches]
        names = [m.group(2) for m in matches]
        namesString = ', '.join(names)
        return (namesString, types)

    # open and read helium report
    reportText = open(report_filename, "r").read()
    reportText = reportText.replace('\r\n', '\n')

    # first element is a syntax guide
    cssReports = reportText.split('Stylesheet: ')[1:]

    # split each report line-by-line to make rules; split each rule by comma
    # each rule is now a list of {Type}name items
    cssReports = [map(lambda rule: rule.split(', '), report.split('\n')) for report in cssReports]

    # extract name of stylesheet
    cssReports = [(report[0][0], report[2:]) for report in cssReports]

    # we split each rule into a "name1, name2, ..." -> [Types] dict
    cssReports = [(name, dict(map(parseRule, report))) for (name, report) in cssReports]

    for report in cssReports:
        improvedCSS = cleanCSS(report)

        # save sheet as [original name]-clean.css
        improvedCSS_filename = cleanSheetForStylesheet(report[0])
        saveMinifiedStylesheetAs(improvedCSS, improvedCSS_filename)

        # print statistics e.g. compression ratio
        if log_statistics:
            # Parse initial stylesheet
            initialCSS_filename = report[0]
            initialCSS = toStylesheet(initialCSS_filename)
            # Print sheet title
            print "* %s:" % initialCSS_filename
            # Call logging function
            logStatistics(initialCSS, improvedCSS)
