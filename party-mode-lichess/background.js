var interval = 3000

task = setInterval(function(){
	var board_style = ["blue","blue3","blue-marble","canvas","wood","wood3","wood4","maple","maple2","brown","leather","green","green-plastic","metal","purple","purple-diag","pink","ic"]
	random_board_style = board_style[Math.floor(Math.random() * board_style.length)]

	var body = document.getElementsByTagName("BODY")[0];
	split_body_className = body.className.split(" ")

	for (style in board_style){
		if(split_body_className.includes(board_style[style]))
		{
			idx = split_body_className.indexOf(board_style[style])
			split_body_className[idx] = random_board_style
			break
		}
	}
	body.className = split_body_className.join(" ")

	var pices_style = ["cburnett","merida","alpha","chessnut","chess7","reillycraig"]
	random_pice_style = pices_style[Math.floor(Math.random() * pices_style.length)]
	document.getElementById('piece-sprite').href = 'https://lichess1.org/assets/_6reABJ/piece-css/'+random_pice_style+'.css'
}, interval);





