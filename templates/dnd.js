function dropenter(event) {
    event.stopPropagation();
    event.preventDefault();
}
function drop(event){
	var dt = event.dataTransfer;
	let files = dt.files;
	for (let i = 0; i < files.length; i++){
		if (files[i].type == "application/pdf")
			appendFile(files[i]);
	}
	event.stopPropagation();
	event.preventDefault();
}
function allow(event){ 
    event.preventDefault();
}
