// Generated by CoffeeScript 1.6.3
var automate, runAutomate;

automate = function(URLs) {
  var status;
  helium.init();
  status = (function() {
    switch (helium.data.status) {
      case 0:
        return "Beginning report";
      case 1:
        return "Gathering list of stylesheets";
      case 2:
        return "Loading stylesheets";
      case 3:
        return "Cross-referencing selectors with DOM";
      case 4:
        return "Complete";
    }
  })();
  console.log(status);
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

runAutomate = function(URLs) {
  if (document.readyState === "complete") {
    return automate(URLs);
  } else {
    return document.addEventListener("load", function() {
      return automate(URLs, false);
    });
  }
};
