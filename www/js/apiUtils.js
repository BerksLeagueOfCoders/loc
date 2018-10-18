export function apiAJAX(opts) {
	return new Promise((resolve, reject)=> {
		var xhr = new XMLHttpRequest();
		xhr.open(opts.method, opts.url);
		xhr.onload = function(){
			if (this.status >= 200 && this.status < 300) {
				resolve(xhr.response);
			} else {
				reject({
					status: this.status,
					statusText: xhr.statusText
				});
			}
		};
		xhr.onerror = function(){
			reject({
				status: this.status,
				statusText: xhr.statusText
			});
			
		};
		if (opts.headers) {
			Object.keys(opts.headers).forEach((key)=>{
				xhr.setRequestHeader(key, opts.headers[key]);
			});
		}
		var params = opts.data;
		// We'll need to stringify if we've been given an object
		// If we have a string, this is skipped.
		if (params && typeof params === 'object') {
			params = Object.keys(params).map((key)=>{
				return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
			}).join('&');
		}
		xhr.send(params);
		
	});
}



export function setCookie(name, value, days) {
	var d = new Date;
	d.setTime(d.getTime() + 24*60*60*1000*days);
	document.cookie = name + "=" + value + ";path=/; expires=" + d.toGMTString();
}
	
	
export function getCookie(name) {
	var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
	return v ? v[2] : null;
}
	
export function deleteCookie(name) {
	setCookie(name, '', -1); 
}