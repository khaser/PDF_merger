let unsortForm = new FormData();
$(function() {
	$( "#sortable" ).sortable();
	$( "#sortable" ).disableSelection();
});

function get_permutation(){
	var idsInOrder = $("#sortable").sortable("toArray");
	return idsInOrder;
};

let cnt = 0;
function appendFile(el) {
	unsortForm.append('files[]', el);
	$("<li id='" + cnt++ + "' class='ui-state-default'>" + el.name + "</li>").appendTo($("#sortable"));
	$("#sortable").sortable({ refresh: sortable });
};

$(document).ready(function() {
	const form = document.getElementById('form2');
	form.addEventListener('submit', e => {
		e.preventDefault();
		let formData = new FormData(); 
		get_permutation().forEach(e => formData.append('files[]', unsortForm.getAll("files[]")[e]));
		
		// $.ajax({
		//     url: '/upload',
		//     data: formData, 
		// 	type: 'POST',
		// 	contentType: false,
		// 	processData: false,
		//     success: function (data, status, xhr) {
		// 		console.log(data)
		// 	    var pdfFile = new Blob([data]);
		// 		const url = URL.createObjectURL(pdfFile);
				
		// 		const dummy = document.createElement('a');
		// 		dummy.href = url;
		// 		dummy.download = 'my-filename.ico';
				
		// 		document.body.appendChild(dummy);
		// 		dummy.click();
		//     }
		// });
		fetch('/upload', {
		    method: 'POST',
		    body: formData,
		})
		.then(response => response.blob())
		.then(blob => {
		    const url = window.URL.createObjectURL(blob);
		    const a = document.createElement('a');
		    a.style.display = 'none';
		    a.href = url;
		    // the filename you want
		    a.download = 'merged.pdf';
		    document.body.appendChild(a);
		    a.click();
		    window.URL.revokeObjectURL(url);
		});
	});
});
