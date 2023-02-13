function multiplyBy()
       {
          num1 = document.getElementById(
            "price").value;
          num2 = document.getElementById(
            "qty").value;
          document.getElementByClass(
            "result").innerHTML = num1 * num2;
       }
