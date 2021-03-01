document.onready = () => {
  const ADDR_BOX = document.getElementById('{{ form.address.id_for_label }}');
  const SEARCH_URL = '/download/search/';
  const ADDR_LIST = document.getElementById('addrlist');
  const STATUS_BOX = document.getElementById('statusbox');
  const FORM = document.getElementById("codeform");
  const SUBMIT_BUTTON = FORM.querySelector("input[type=submit]");
  // from W3CSchools
  function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
  var c = ca[i];
  while (c.charAt(0) == ' ') {
    c = c.substring(1);
  }
  if (c.indexOf(name) == 0) {
    return c.substring(name.length, c.length);
  }
  }
  return "";
  }
  // form MDN

  function sendData( data ) {
  const XHR = new XMLHttpRequest(),
      FD  = new FormData(FORM);

  // Push our data into our FormData object
  for( name in data ) {
  FD.append( name, data[ name ] );
  }

  // Define what happens on successful data submission
  XHR.addEventListener( 'load', function( event ) {
  resp = JSON.parse(event.target.response);
  if (resp.status === 'OK') {
    STATUS_BOX.style.color = 'white';
    STATUS_BOX.innerText = 'Success! Please check your inbox.';
    SUBMIT_BUTTON.value = 'Success!';
  } else {
    STATUS_BOX.innerText = 'Error: ' + resp.message;
    STATUS_BOX.style.color = 'red';
  }
  } );

  // Define what happens in case of error
  XHR.addEventListener(' error', function( event ) {
  alert( 'Oops! Something went wrong.' );
  } );

  // Set up our request
  XHR.open( 'POST', "{% url 'download' %}");
  XHR.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

  // Send our FormData object; HTTP headers are set automatically
  XHR.send( FD );
  }

  const remFakeHover = () => {
    for (ele of ADDR_LIST.getElementsByTagName('li')) {
      ele.classList.remove('fake-hover');
    }
  }
  const fakeHover = (i) => {
    remFakeHover();
    let ele = ADDR_LIST.getElementsByTagName('li')[i];
    ele.classList.add('fake-hover');
  }
  var selected_item = -1;
  ADDR_BOX.onkeydown = async (e) => {
    console.log(selected_item);
    let update = false;
    if (e.key === 'ArrowDown') {
      selected_item++;
      update = true;
    } else if (e.key === 'ArrowUp') {
      selected_item--;
      update = true;
    } else if (e.key === 'Enter' || e.key === 'Space') {
      e.preventDefault();
      ADDR_LIST.getElementsByTagName('li')[selected_item].click();
    }
    if (update) {
      fakeHover(selected_item);
    }
  };
  ADDR_BOX.oninput = async (e) => {
    const ADDR_INPUT = e.target.value;
    console.log(e.target.value);

    let response = await fetch(SEARCH_URL + ADDR_INPUT);
    let addresses = await response.json();
    console.log(addresses);
    ADDR_LIST.innerHTML = '';
    let ul = document.createElement('ul');
    ul.classList.add('semantic');
    for (var i = 0; i < addresses.length; i++) {
      let address = addresses[i];
      let li = document.createElement('li');
      li.innerText = address.address;
      li.onclick = function(e) {
        console.log(e.target.innerText);
        ADDR_BOX.value = e.target.innerText;
        ADDR_BOX.readOnly = true;
        ADDR_LIST.innerHTML = '';
        // focus on next input box; depends on layout
        document.getElementById('{{ form.code.id_for_label }}').focus();
      }
      ul.appendChild(li);
    }
    ADDR_LIST.appendChild(ul);
  }
  FORM.addEventListener('submit', (e) => {
    e.preventDefault();
    sendData();
  });
}
