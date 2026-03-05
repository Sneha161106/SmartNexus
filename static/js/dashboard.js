async function loadIncidents(){

let response = await fetch("/incidents");

let data = await response.json();

let labels = []
let scores = []

data.forEach(e=>{
labels.push(e.Time)
scores.push(e.ThreatScore)
})

chart.data.labels = labels
chart.data.datasets[0].data = scores

chart.update()

}

setInterval(loadIncidents,2000)