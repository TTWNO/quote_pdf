// Warning, manual IDs
const ADDR_BOX = document.getElementById('id_address');
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
  STATUS_BOX.innerText = '';
  SUBMIT_BUTTON.value = 'Success!';
  SUBMIT_BUTTON.style.backgroundColor = '#61F900';
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
XHR.open( FORM.getAttribute('method'), FORM.getAttribute('action'));
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
  var addresses;
  var has_results = false;
  try {
    addresses = await response.json();
  } catch {
    addresses = '';
  }
  console.log(addresses);
  ADDR_LIST.innerHTML = '';
  ADDR_LIST.style.border = 'none';
  let ul = document.createElement('ul');
  ul.classList.add('semantic');
  for (var i = 0; i < addresses.length; i++) {
    const address = addresses[i];
    has_results = true
    let li = document.createElement('li');
    li.innerText = address.address;
    li.onclick = function(e) {
      console.log(e.target.innerText);
      ADDR_BOX.value = e.target.innerText;
      ADDR_LIST.innerHTML = '';
      ADDR_LIST.style.border = 'none';
      // focus on next input box; depends on layout
      document.getElementById('id_code').focus();
    }
    ul.appendChild(li);
  }
  if (has_results) {
    ADDR_LIST.appendChild(ul);
    ADDR_LIST.style.border = '1px solid black';
  } else {
    ADDR_LIST.style.border = 'none';
  }
}
const clearFields = () => {
  FORM.reset();
}
FORM.addEventListener('submit', (e) => {
  e.preventDefault();
  sendData();
  clearFields();
});
