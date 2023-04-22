/*!
 * 
 * JavaScript for Campo RUT para Contact Form 7
 * 
 */


/**
 * ------------------------------------------------------------------------
 * Ready function
 * ------------------------------------------------------------------------
 */

function cf7rf_ready(callback){
  // in case the document is already rendered
  if (document.readyState!='loading') callback();
  // modern browsers
  else if (document.addEventListener) document.addEventListener('DOMContentLoaded', callback);
  // IE <= 8
  else document.attachEvent('onreadystatechange', function(){
      if (document.readyState=='complete') callback();
  });
}

/**
 * ------------------------------------------------------------------------
 * Field filter
 * ------------------------------------------------------------------------
 */

function cf7rf_setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
    if (inputFilter(this.value)) {
      this.oldValue = this.value;
      this.oldSelectionStart = this.selectionStart;
      this.oldSelectionEnd = this.selectionEnd;
    } else if (this.hasOwnProperty("oldValue")) {
      this.value = this.oldValue;
      this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
    } else {
      this.value = "";
    }
    });
  });
}


/**
 * ------------------------------------------------------------------------
 * Format RUT
 * ------------------------------------------------------------------------
 */

function cf7rf_formatRut(rut) {
 var rut = rut.replace(/^0+/, "");
  if (rut != '' && rut.length > 1) {
      var rut = rut.replace(/\./g, "");
      var rut = rut.replace(/-/g, "");
      var dv = rut.substring(rut.length - 1);
      var rut = rut.substring(0, rut.length - 1);
      var rutPoints = "";
      var i = 0;
      var j = 1;
      for (i = rut.length - 1; i >= 0; i--) {
          var c = rut.charAt(i);
          rutPoints = c + rutPoints;
          if (j % 3 == 0 && j <= rut.length - 1) {
            rutPoints = "." + rutPoints;
          }
          j++;
      }
      rutPoints = rutPoints + "-" + dv;
      return rutPoints;
  }else{
    return null;
  }
}


/**
 * ------------------------------------------------------------------------
 * Callback ready
 * ------------------------------------------------------------------------
 */

cf7rf_ready(function(){
  if(typeof document.getElementsByClassName('wpcf7-form')[0] !== 'undefined' && document.getElementsByClassName('wpcf7-form')[0] !== null){
    if(typeof document.getElementsByClassName('wpcf7-validates-as-rut')[0] !== 'undefined' && document.getElementsByClassName('wpcf7-validates-as-rut')[0] !== null){
      var fields = document.getElementsByClassName('wpcf7-validates-as-rut');
      for (var i = 0; i < fields.length; ++i) {
        var field = fields[i];
        if(field.classList.contains("wpcf7-rut-onlynumbers")){
          cf7rf_setInputFilter(field , function(value) {return /^[0-9kK]*$/.test(value); });
        }
        field.addEventListener("blur", blurCallback, false);
      }
      function blurCallback(e) {
        var field = e.currentTarget
        var value = field.value;
        if(typeof value  !== 'undefined' && value != '' && value != null){
          if(field.classList.contains("wpcf7-rut-onformat")){
            field.value = cf7rf_formatRut(value);
          }
        }
      }
    } 
  }

});