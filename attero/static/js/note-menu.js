$(function() {
    $('#tree1').tree({
	dragAndDrop: true,
	autoOpen: 0,
	saveState: true,
	selectable: true,
    });

//$('#tree1').bind(
//    'tree.contextmenu',
//    function(event) {
//        // The clicked node is 'event.node'
//        var node = event.node;
//        alert(node.name);
//    }
//);


$('#tree1').bind(
    'tree.move',
    function(event) {
        event.preventDefault();

        if (confirm('Really move this note?')) {
            //event.move_info.do_move();
	    alert('This feature is incomplete');
	    //$.post('your_url', {tree: $(this).tree('toJson')});
        }
    }
);


$('#tree1').bind(
    'tree.click',
    function(event) {
        // The clicked node is 'event.node'
        var node = event.node;
	window.location.href = node.url;
    }
);



});
