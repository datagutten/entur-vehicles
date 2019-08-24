//http://student.cs.hioa.no/hovedprosjekter/data/2012/13/dokumentasjon.htm
const x = document.getElementById('error');
$("#holdeplass").keyup(function (event) {
    if (event.target.value.length > 1) {
        $("#stops").load(autocomplete_url + "?text=" + event.target.value);
    }
});

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(find_stops_by_location, showError);
    } else {
        x.innerHTML = "Geolokasjon er ikke st&oring;ttet av denne nettleseren.";
    }
}
$("#get_location").click(getLocation());

function find_stops_by_location(position) {
    $('#stops').load(stops_latlon_url + "?lat=" + position.coords.latitude + "&lon=" + position.coords.longitude);
    console.log(position);
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            x.innerHTML = "Bruker godtok ikke forespørselen om posisjonstilgang.";
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Posisjonsinformasjon er ikke tilgjengelig";
            break;
        case error.TIMEOUT:
            x.innerHTML = "Forespørselen om posisjon fikk tidsavbrudd";
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "En ukjent feil oppstod";
            break;
    }
}
