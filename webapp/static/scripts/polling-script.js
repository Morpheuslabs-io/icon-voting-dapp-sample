var pageURL = window.location.href;
var walletName = pageURL.substr(pageURL.lastIndexOf('/') + 1);

localStorage.setItem("wallet", walletName);


$(function () {
	$('#vote').click(function () {
		var polledValue = document.querySelector("input[name='winnerRadio']:checked").value
		console.log("polledValue :" + polledValue);
		$.ajax({
			url: '/vote/' + localStorage.getItem("wallet"),
			data: {
				'element': polledValue
			},
			type: 'POST',
			success: function (response) {
				console.log(response);
				jsonResponse = JSON.parse(response);
				alert(jsonResponse.message);
			},
			error: function (error) {
				console.log(error);
			}
		});
	});

	function getMyVote() {
		$.ajax({
			url: '/myVote/' + localStorage.getItem("wallet"),
			type: 'GET',
			success: function (response) {
				console.log('myVote: ' + response);
				document.getElementById("myVoteResult").innerText = response;
				if (response == 'YES') {
					document.getElementById("vote").disabled = true;
					document.getElementById("vote").classList.add("btn-info");
					document.getElementById("vote").classList.add("disabled");
				}
			},
			error: function (error) {
				console.log(error);
			}
		});
	}

	function getAllVotesIcon() {
		$.ajax({
			url: '/result/' + localStorage.getItem("wallet"),
			type: 'GET',
			success: function (response) {
				console.log(response);
				jsonResponse = JSON.parse(response);
				document.getElementById("totalVotesYes").innerText = jsonResponse['yes'];
				document.getElementById("totalVotesNo").innerText = jsonResponse['no'];
				getMyVote();
				loadChart(jsonResponse);
			},
			error: function (error) {
				console.log(error);
			}
		});
	};
	getAllVotesIcon();
	$('#getAllVotes').click(function () {
		getAllVotesIcon()
	});

	function loadChart(response) {
		document.getElementById("totalVotes").innerText = +response['yes'] + +response['no'];
		var ctx = document.getElementById("myChart").getContext('2d');
		var myChart = new Chart(ctx, {
			type: 'pie',
			data: {
				labels: ["Yes", "No"],
				datasets: [{
					label: '# Yes vs No Vote',
					data: [response['yes'], response['no']],
					backgroundColor: [

						'rgba(54, 162, 235, 0.4)',
						'rgba(255, 99, 132, 0.4)'

					],
					borderColor: [
						'rgba(54, 162, 235, 1)',
						'rgba(255,99,132,1)',

					],
					borderWidth: 1
				}]
			},
			options: {
			}
		});


	}
});