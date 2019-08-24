function rangecheck(value,low,high)
{
	if(value>=low && value<=high)
		return true;
	else
		return false;
}
function expectedVechile(vechile,line)
{
	var unexpected=false;;
	if(line==83 && vechile!='Volvo 8700')
	{
		unexpected=true;
	}
	return unexpected;
}
function checkVechiles()
{
	var departures=document.getElementsByClassName('item');
	var departure;
	var key;
	var vechile;
	var vechileNumber;
	var vechileInfo;

	for (var i=0; i<departures.length; i++)
	{
		departure=departures.item(i);
		key=departure.id;
		vechile=departure.childNodes.item(4);
		vechileNumber=Number(vechile.textContent);
		vechileInfo=vechileType(vechileNumber);
		
		var lineNumber=departure.parentNode.parentNode.childNodes.item(1).childNodes.item(1).textContent;
		
		if(vechileInfo[1]!==false && vechileInfo[1].indexOf(lineNumber)<0)
		{
			vechile.setAttribute('style','color: #FF0000');
		}
	}
}
function vechile_onclick(vechile_num,line,operator,object)
{
	
	var type=vechileType(vechile_num);
	
	/*if(type[1]===false)
	{
		alert(type[0]+"\n");
	}
	else
	{*/
	/*if(type[1].indexOf(line)<0)
	{
		alert(type[0]+"\nDenne busstypen er ikke forventet på linje "+line);
	}
	else*/
	{
		get_vechile_info(vechile_num,line);
	}
	//}
}


function get_vechile_info(vechile_num,line)
{
	var xhttp=new XMLHttpRequest();
	xhttp.open('GET','materiell_find.php?vehicle='+vechile_num+'&line='+line,true);
	//xhttp.open('GET',':8000/vehicles/expected_vehicle/line/'+line+'/vehicle/'+vechile_num);
	xhttp.send();

	xhttp.onreadystatechange = function()
	{
	  if (xhttp.readyState === 4 && xhttp.status === 200)
	  {
		//document.getElementById("demo").innerHTML = xhttp.responseText;
		//var vechile=JSON.parse(xhttp.responseText);
		//alert(vechile.operator+' '+vechile.type+' '+vechile.length+'m '+vechile.year);
		alert(xhttp.responseText);
	  }
	};
}

