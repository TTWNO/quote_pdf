window.onload = () => {
    const addresses_ul = document.getElementById(UL_ID);
    const addrinput = document.getElementById(ADDRESS_ID);

    const delete_possible = () => {
        addresses_ul.innerHTML = "";
    };
    const update_input = async (e) => {
        addrinput.value = e.target.value;
    };

    const set_founds = (addrs) => {
        console.log("DEBUG:");
        console.log(addrs);

        addresses_ul.innerHTML = "";
        // add a button within an li for each returned address
        for (addr of addrs) {
            addri = document.createElement('li');
            addrb = document.createElement('button');
            addrb.innerText = addr['address'];
            addrb.value = addr['address'];
            addrb.addEventListener('click', update_input);
            addrb.addEventListener('click', delete_possible);
            addri.appendChild(addrb);
            addresses_ul.appendChild(addri);
        }
    };
    const check = async (e) => {
        const val = e.target.value;
        console.log(val);

        let response = await fetch('/upload/search/' + val + '/')
            .then(response => response.json())
            .then(response => set_founds(response));
    }
    addrinput.addEventListener('input', check);
}
