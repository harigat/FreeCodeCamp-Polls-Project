var colortimes=function(data){
	length=data.length
	list=[]
	for(var i=1;i<=length;i++){
		list.push('#' + (Math.random().toString(16) + '0000000').slice(2, 8) )
	}
	return list
}
var ctx = document.getElementById("myChart");
var colors=colortimes(votes);
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: choices,
        datasets: [{
            //label: '# of Votes',
            data: votes,
            backgroundColor: colors,
            borderColor: colors,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
alert(votes);