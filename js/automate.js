// Generated by CoffeeScript 1.6.3
var automate;

automate = function(URLs) {
  if (helium.data.status === 0) {
    return setTimeout(function() {
      if (document.querySelector('#cssdetectTextarea')) {
        document.querySelector('#cssdetectTextarea').innerHTML = URLs;
        $('#cssdetectStart').click();
        return location.reload();
      }
    }, 2000);
  } else if (helium.data.status === 4) {
    return setTimeout(function() {
      if ($("#cssreportDownloadReport").is(':visible')) {
        $('#cssreportResetID').click();
        return location.reload();
      }
    }, 2000);
  }
};
