/*
http://sketch.paperjs.org/#V/0.12.15/S/hVRta9swEP4rh7/Ebj3H7VgGyTIIa2GFpQTSsEISgmIrkYktGVluakL/+06SndiBMn+RfPfc63Onk8NJRp2hMz9QFTHHdyIR6/83IiEXhapSCmM4wS5J018iFXLY20ta9XwolBQHamXQ26YkOvQ+VnLFtenxiFaxiMqMchVsRVwFUZrg/W8SK9agGPsE9Zsme6Y0LBK8UPC8mG7mk+nsz+McLe7C8KKaTl43WvP0snh4ROXX+++DwUWdVRMpSYUKTo9g7m7LmxfowtzQa1JStFBCV2xKAfx2JY9UIjjMRMJV8SJmRDE3Nz8enBqY/kzTUFtHy0lOZWDgXhu2ExJcjU0QGI7w+AHWX5BSvldMi26xziv35xBoZvHLZD26RugEAhLHbisFDXbzZbj2IV/erb1OOqbStsB4iFJR0BgjKVnSThBJVSm5QTXis4tzswSfirKgD5LsXfqGlLZqMX1m9BWdT3UoKUoeu0VEUmqxgakuePch9HGUzNEi7eb+UkC/D0j0rtS5kq0oFRxZBU/ASAxIZCzKLU5we34wsqSNeT0eS53O+n/5VCYRxszRmTubz0pdDYClfmR1pqutpUFMvTWjpns1SJPXittx0BBrKb3ulmexn9KxyGsyzlzoLREpDVKxd+tmeB0Xdo1MMzBjl5eZDwnfZAm3J8G42HYrMBfy7sH4Z0N3PS3aEL7Ulh7cgFtjUVibe9AH17psIW8b9aWyft+0QtJMvFG7Wij6di0YdAS1kBEVmFdtXL9u+ORtJSUHu1DOcLn++Ac=
*/
var postyle = { fillColor:'grey', strokeColor: 'black'}
var ww = document.body.clientWidth
var hh = document.body.clientHeight
const NUM_SAMPLES = 100
const MAX_AMPLITUDE = 32766
const myArray = new Array(NUM_SAMPLES).fill(0)
var testo = {}
    function PointsToPath(points) {
        var path = new paper.Path()
        for (var i = 0; i < points.length; i += 1) {
            var p = points[i];
            path.add(new paper.Point(p[0], p[1]))
        }

        path.closed = true;
        return path
    }

function onMouseDrag(event) {
    var theX = Math.round(scale(event.point.x, 0, ww, 0, NUM_SAMPLES*2))
    // confused about why I had to double NUM_SAMPLES there
    myArray[theX] = Math.round(scale(event.point.y, 0, hh, 0, MAX_AMPLITUDE))
	var path = new Path();
	path.strokeColor = 'black';

	path.add(event.point);
	path.add(new Point(event.point.x, 0));
}

function onMouseUp(event){
    console.log(myArray)
}

const scale = (num, in_min, in_max, out_min, out_max) => {
  return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
//path.remove()
//p5.remove()
//p6.remove()

//phat.style=postyle