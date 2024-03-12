function submitForm() {
    var field1Value = document.getElementById("field1").value;
    var field2Value = document.getElementById("field2").value;
 
    console.log("Значення полів:");
    console.log("Поле 1: " + field1Value);
    console.log("Поле 2: " + field2Value);
 }
 window.addEventListener('keydown', function(event) {
          if (event.ctrlKey && (event.key === '+' || event.key === '=' || event.key === '-' || event.key === '_')) {
              event.preventDefault();
          }
      });