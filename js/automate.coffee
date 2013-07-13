automate = (URLs) ->
  ##
  # If Helium is clear, inject target pages.
  # If Helium is in final stages, get ready to download report.
  # And if Helium has a complete report, restart process.
  ##
  if helium.data.status == 0
    setTimeout ->
      if document.querySelector '#cssdetectTextarea'
        document.querySelector('#cssdetectTextarea').innerHTML = URLs
        $('#cssdetectStart').click()
        location.reload()
    , 2000
  else if helium.data.status == 4
    setTimeout ->
      if $("#cssreportDownloadReport").is ':visible'
        $('#cssreportResetID').click()
        location.reload()
    , 2000