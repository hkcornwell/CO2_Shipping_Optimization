if (!window.dash_clientside) {
  window.dash_clientside = {};
}
window.dash_clientside.clientside = {
  resize: function(value) {
    setTimeout(function() {
      window.dispatchEvent(new Event("resize"));
      console.log("fired resize");
    }, 500);
    return null;
  }
};
