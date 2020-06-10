let unsortForm = new FormData();
let fl = new Array();

$(function() {
	$( "#sortable" ).sortable();
	$( "#sortable" ).disableSelection();
});

$( "#sortable" ).disableSelection();

function get_permutation(){
	var idsInOrder = $("#sortable").sortable("toArray");
	return idsInOrder;
};

let cnt = 0;
function appendFile(el) {
	unsortForm.append('files[]', el);
	fl.push(0);	
	$("<li id='" + cnt + "' class='ui-state-default'>" + el.name + "<img src='/static/delete.png' height='20' align='right' onclick='deleteFile(" + cnt + ")'> </li>").appendTo($("#sortable"));
	cnt++;
	$("#sortable").sortable({ refresh: sortable });
};

function deleteFile(number) {
	for (let i = 0; i < $('ul li').length; ++i) {
		if ($('ul li')[i].id == number) {
			$('ul li')[i].hidden = 1;
			fl[$('ul li')[i].id] = 1
		}
	}
}

$(document).ready(function() {
	const form = document.getElementById('form2');
	form.addEventListener('submit', e => {
		e.preventDefault();
		let formData = new FormData(); 
		get_permutation().forEach(e => {
			if (fl[e] == 0) {
				formData.append('files[]', unsortForm.getAll("files[]")[e]);
			}
		});
		
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
