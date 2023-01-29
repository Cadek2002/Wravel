import wixData from 'wix-data';
import {getJSON} from 'wix-fetch';
import {getInfo} from 'backend/getGCapi'
const urlBase = 'https://wravel-get-info-5f767tw2ea-uc.a.run.app/?country=';

$w.onReady(function () {


});

export async function search(){
	let url = (String)(urlBase)+(String)($w('#countryField').value)
	const response = await getJSON(url, {'method' : 'get'});
	return response;
}

export async function updateCards(apiAdd, key) {
	let json = await getInfo(apiAdd, key)
	console.log(json)
}



export function countryField_change(event) {
	if ($w('#countryField').value != "")
		search(urlBase, $w('#countryField').value);
}

