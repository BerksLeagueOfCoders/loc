"use strict";
window.addEventListener('load', function() {

	var xhttp = new XMLHttpRequest(); 
	xhttp.open("GET", "http://localhost:5001/league-of-coders-e5791/us-central1/test", true);
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			const t_div=document.querySelector("#CONTENT_HERE");
			const t_template=document.querySelector("template#PROJECT_TEMPLATE");
			JSON.parse(this.responseText).projects.forEach(function(x) {
				const clone = t_template.content.cloneNode(true);
				clone.querySelector("span").innerHTML=x.name+" Project";	
				clone.querySelector("img").src+=x.img;	
				clone.querySelector("p").innerHTML+=x.desc;	
				clone.querySelector("a").href+=x.dirName+"/";	
				t_div.appendChild(clone);
				
			});
		}
		
	};
	xhttp.send();
	
});