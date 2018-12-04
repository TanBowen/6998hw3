$(document).ready(function() {
	$("#upload_button").click(() => {
		var f = $('#file_input').prop('files')[0];
		if (f) {
			console.log(f.name);
			console.log(f.type);
			console.log(f.size);
			if (!f.type.match('image.*')) {
				alert("Must be image");
				return false;
			}
			var xhr = new XMLHttpRequest(); 
			xhr.open("PUT", "https://tpgm3w6oma.execute-api.us-east-1.amazonaws.com/stage1/upload?object=" + f.name);
			xhr.setRequestHeader("Content-Type", f.type);
			xhr.setRequestHeader("x-api-key", "53ZyTeRZRoafGfbcZkVKl7albvbexDgo2X9m3gY1");
			// xhr.onload = function (event) { 
			// };
			xhr.send(f);
		}
		else {
			alert("Please first select a file");
		}
	});
	$("#search_button").click(() => {
		var q = $('#search_query').val();
		console.log(q);
		// var apigClient = apigClientFactory.newClient();
		var apigClient = apigClientFactory.newClient({
			apiKey: "53ZyTeRZRoafGfbcZkVKl7albvbexDgo2X9m3gY1"
		});
		var params = {
			//This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
			q: q
		};
		var body = {
			//This is where you define the body of the request
			// "q": q
		};
		var additionalParams = {
			//If there are any unmodeled query parameters or headers that need to be sent with the request you can add them here
		};
		apigClient.searchGet(params, body).then(function(result){
			//This is where you would put a success callback
			console.log(result);
			console.log("worked!!")
			console.log(result.data.results)
			console.log(result);
		}).catch(function(result) {
			//This is where you would put an error callback	
			console.log(result);
		});
	});
});




