function vehicle_type(vehicle_num) {
    const request = new XMLHttpRequest();
    request.open('GET', '/vehicle/' + vehicle_num + '.json', true);

    request.onload = function() {
      if (this.status >= 200 && this.status < 400) {
        // Success!
        const data = JSON.parse(this.response);
        if (data['error']!=='') {
            alert(data['error']);
        }
        else {
            alert(data['string']);
        }

        console.log(data)
      } else {
        // We reached our target server, but it returned an error

      }
    };

    request.onerror = function() {
      // There was a connection error of some sort
    };

    request.send();
}