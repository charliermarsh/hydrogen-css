##
# Wait until the test condition is true or a timeout occurs. Useful for waiting
# on a server response or for a ui change (fadeIn, etc.) to occur.
#
# @param testFx javascript condition that evaluates to a boolean,
# it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
# as a callback function.
# @param onReady what to do when testFx condition is fulfilled,
# it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
# as a callback function.
# @param timeOutMillis the max amount of time to wait. If not specified, 3 sec is used.
##
waitFor = (testFx, onReady, timeOutMillis = 3000, failureMsg = '\'waitFor\' timeout', successMsg = '\'waitFor\' success.') ->
  start = new Date().getTime()
  condition = false
  f = ->
    if (new Date().getTime() - start < timeOutMillis) and not condition
      # If not time-out yet and condition not yet fulfilled
      condition = (if typeof testFx is 'string' then eval testFx else testFx()) #< defensive code
      console.log page.evaluate -> return helium.data.status
    else
      if not condition
        # If condition still not fulfilled (timeout but condition is 'false')
        console.log failureMsg
        phantom.exit 1
      else
        # Condition fulfilled (timeout and/or condition is 'true')
        console.log successMsg + " in #{new Date().getTime() - start}ms."
        if typeof onReady is 'string' then eval onReady else onReady() #< Do what it's supposed to do once the condition is fulfilled
        clearInterval interval #< Stop this interval
  interval = setInterval f, 250 #< repeat check every 250ms

# load requirements
fs = require 'fs'
system = require 'system'

# make sure user has provided correct args
if system.args.length < 2
  console.log "Target URL required"
  phantom.exit()
url = system.args[1]

# create page
page = require('webpage').create();

# load page from url
page.open url, (status) ->
  if status isnt 'success'
    console.log 'Failed to load page.'
    phantom.exit()
  # inject page w/ JS: jQuery, automate, helium
  if not page.injectJs('jquery.min.js') or not page.injectJs('helium.js') or not page.injectJs('automate.js')
    console.log "Failed to load JavaScript"
    phantom.exit()
  page.evaluate -> automate(document.URL)
  # wait for button to be visible
  waitFor ->
    page.evaluate ->
      $("#cssreportDownloadReport").is ':visible'
  , ->
    report = page.evaluate ->
      # get URL with report encoded
      a = $("#cssreportDownloadReport").attr 'href'
      encoded_data = a.split(',')[1]
      decoded_data = decodeURIComponent escape window.atob encoded_data
      return decoded_data
    # try to write report to file; else, echo to console
    try
      fs.write system.args[2], report, "w"
    catch e
      console.log report
    phantom.exit()
  , 30000
  , "Error generating report."
  , "Report generated"
