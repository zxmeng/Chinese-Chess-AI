var HighlightPiece = cc.DrawNode.extend({
	ctor: function() {
		this._super();		
		this.width = 55;
		this.height = 55;
	},
	init_circle: function() {
		var color = new cc.Color(0, 0, 255, 100);
		this.drawDot(cc.p(0, 0), this.width/2, color);
	},
	onEnter: function() {
		this.init_circle();
	}
});

var ChessPiece = cc.Node.extend({
	piece_name: null,
	clicked: false,
	startPoint: false,
	color: null,
	piece_type: null,
	board_position: {row: 0, col:0},
	last_board_position: {},
	ctor : function(piece_name) {
		this._super();
		this.piece_name = piece_name;
		var ss = piece_name.split('_');
		this.color = ss[0];
		this.piece_type = ss[1];
		this.load_image(piece_name);
	},
	load_image : function(piece_name) {
		var sprite_name = '#' + piece_name + '.png';
		var sprite = cc.Sprite.create(sprite_name);
		this.addChild(sprite);
		this.width = sprite.width;
		this.height = sprite.height;
	},
	is_clicked: function(point) {
		var distance = cc.pDistance(point, this);
		return (distance <= this.width/2);
	},
	set_board_position: function(row, col) {
		this.board_position = {row: row, col: col};	
	},
	save_last_position: function() {
		this.startPoint = cc.p(this.x, this.y);
		this.last_board_position = {row: this.board_position.row, col: this.board_position.col};
	},
	go_last_position: function() {
		if (this.startPoint) {
			this.setPosition(this.startPoint);
		}
	}
});

var PieceLayer = cc.Layer.extend({
	chess_board : null,
	chess_pieces: [],
	up_captured_pieces: [],
	down_captured_pieces: [],
	highlight_points: [],
	possible_move: [],
	selected_piece: null,	
	down_side: "red",
	current_side: "red",
	clock_layer: null,
	hud_layer: null,
	game_running: false,
	ctor : function(chess_board) {
		this._super();
		this.chess_board = chess_board;		
		this.init_input();
	},
	init_input: function() {
		cc.eventManager.addListener({
            event: cc.EventListener.MOUSE,            
            //onMouseDown: this.onMouseDown,
            onMouseMove: this.onMouseMove,
        }, this);
        
        cc.eventManager.addListener({
            event: cc.EventListener.TOUCH_ONE_BY_ONE,
            swallowTouches: true,
            onTouchBegan: this.onTouchBegan,
            onTouchMoved: this.onTouchMoved
        }, this);
	},
	reset_piece: function() {
		var i = 0;				
		for (i = 0; i<this.chess_pieces.length; i++) {
			this.removeChild(this.chess_pieces[i]);
		}
		for (i = 0; i<this.up_captured_pieces.length; i++) {
			this.removeChild(this.up_captured_pieces[i]);
		}
		for (i = 0; i<this.down_captured_pieces.length; i++) {
			this.removeChild(this.down_captured_pieces[i]);
		}
		this.chess_pieces = [];
		this.up_captured_pieces = [];
		this.down_captured_pieces = [];
		this.selected_piece = null;
		var change_side = this.down_side == "red" ? "red" : "black";		
		this.chess_board.init_board();
		this.init_piece(change_side);
		this.current_side = "red";
	},
	onMouseDown: function(event) {
		var _this = event.getCurrentTarget();
		var location = event.getLocation();
		if (!_this.selected_piece) {
			_this.up_piece(location);	
		}	
		else {
			_this.down_piece(location);
		}
	},
	onMouseMove: function(event) {
		var _this = event.getCurrentTarget();
		if (_this.selected_piece) {
			_this.selected_piece.setPosition(event.getLocation());
		}
	},
	
	onTouchBegan:function(touch, event) {
        var location = touch.getLocation();
        var _this = event.getCurrentTarget();
		//var location = event.getLocation();
		if (!_this.selected_piece) {
			_this.up_piece(location);	
		}	
		else {
			_this.down_piece(location);
		}
        return true;
    },

    onTouchMoved:function(touch, event) {
        var location = touch.getLocation();
        var _this = event.getCurrentTarget();
		if (_this.selected_piece) {
			_this.selected_piece.setPosition(location);
		}
    },
	up_piece: function(location) {
		var check_piece = this.get_clicked_piece(location);
		if (check_piece) {
			if (check_piece.color == this.current_side) {
				this.selected_piece = check_piece;
				var board_location = this.chess_board.convertToNodeSpace(this.selected_piece);
				var distance = this.chess_board.point_distance;
				var row = Math.round(board_location.y / distance);
				var col = Math.round(board_location.x / distance);
				
				this.selected_piece.save_last_position();
				this.selected_piece.setScale(1.3);
				this.selected_piece.setLocalZOrder(999);
				var possible_move = this.chess_board.get_possible_move(row, col);
				this.highlight_move(possible_move);
				this.possible_move = possible_move;	
				var sid = cc.audioEngine.playEffect(res.ChessPick_mp3);
				cc.director.getScheduler().scheduleCallbackForTarget(this, function() {cc.audioEngine.stopEffect(sid);}, 1, 0, 0, false);
			}
		}
	},
	down_piece: function(location) {
		var board_location = this.chess_board.convertToNodeSpace(location);
		var distance = this.chess_board.point_distance;
		var row = Math.round(board_location.y / distance);
		var col = Math.round(board_location.x / distance);
		var placed = false;
		if (row>=0 && row<this.chess_board.board_height && col>=0 && col<this.chess_board.board_width) {
			var last_row = this.selected_piece.last_board_position.row;
			var last_col = this.selected_piece.last_board_position.col;
			if (last_row != row || last_col !=col) {
				if (this.is_valid_move(row, col)) {
					var enemy_piece = this.chess_board.board_map[row][col];
					if (enemy_piece != null) {
						this.capture_piece(enemy_piece);
					}
					this.selected_piece.setPosition(this.chess_board.get_point_at(row, col));
					console.log(row);
					console.log(col);
								
					this.set_board_map(this.selected_piece, row, col);
					
					this.set_board_map(null, last_row, last_col);			
					this.selected_piece.set_board_position(row, col);
					
					placed = true;
					this.current_side = this.current_side == "red" ? "black" : "red";
					this.clock_layer.pause_time();
					var sid = cc.audioEngine.playEffect(res.ChessMove_mp3);
					cc.director.getScheduler().scheduleCallbackForTarget(this, function() {cc.audioEngine.stopEffect(sid);}, 1, 0, 0, false);
					//cc.audioEngine.stopEffect(sid);
					if (enemy_piece!=null) {
						if (enemy_piece.piece_type == "king") {
							this.hud_layer.visible = true;
							this.clock_layer.reset_clock();
							this.game_running = false;
						}
					}
				}
			}												
		}
		if (!placed) {
			this.selected_piece.go_last_position();
		}
		this.selected_piece.setScale(1);
		this.selected_piece.setLocalZOrder(5);		
		this.selected_piece = null;
		this.clear_highlight();
		// call function for pc to move
		if (placed){
			this.pc_move();
		}

	},
	pc_move: function () {
		// send msg to socket
		var fen = "";
		var piece_name = "";
		for (var r = 9; r >= 0; r--) {
			for (var c = 0; c <= 8; c++) {
				if(this.chess_board.board_map[r][c] == null){
					fen += '1';
				}
				else{
					piece_name = this.chess_board.board_map[r][c].piece_name;
					switch(piece_name) {
						case "black_chariot":
							fen += "r";
							break;
						case "black_knight":
							fen += "n";
							break;
						case "black_elephant":
							fen += "b";
							break;
						case "black_guard":
							fen += "a";
							break;
						case "black_king":
							fen += "k";
							break;
						case "black_cannon":
							fen += "c";
							break;
						case "black_pawn":
							fen += "p";
							break;

						case "red_chariot":
							fen += "R";
							break;
						case "red_knight":
							fen += "N";
							break;
						case "red_elephant":
							fen += "B";
							break;
						case "red_guard":
							fen += "A";
							break;
						case "red_king":
							fen += "K";
							break;
						case "red_cannon":
							fen += "C";
							break;
						case "red_pawn":
							fen += "P";
							break;
					}

				}
			}
			fen += "/";
		}
		fen += "b";
		var socket=io.connect()
		socket.emit("chat",fen)
		//socket.emit('forceDisconnect');
		//socket.disconnect()
		// function sleep(milliseconds) {
  // 		var start = new Date().getTime();
  // 		for (var i = 0; i < 1e7; i++) {
  //   		if ((new Date().getTime() - start) > milliseconds){
  //    		 break;
  //   	}
  // 		}
		// }
		_this=this;
		console.log(fen);
		string = ''
		socket.on('chat1',function (data) {
			console.log(data);
			if(data.length==4){
				string=data;
				console.log(string);
			}


		// waiting for socket message
		row = 9-parseInt(string[0]);
		col = parseInt(string[1]);
		console.log(row);
		//select a piece
		var check_piece = _this.chess_board.board_map[row][col];
		if (check_piece) {
			if (check_piece.color == _this.current_side) {
				_this.selected_piece = check_piece;
				
				_this.selected_piece.save_last_position();
				_this.selected_piece.setScale(1.3);
				_this.selected_piece.setLocalZOrder(999);
				var possible_move = _this.chess_board.get_possible_move(row, col);
				_this.highlight_move(possible_move);
				_this.possible_move = possible_move;	
				var sid = cc.audioEngine.playEffect(res.ChessPick_mp3);
				cc.director.getScheduler().scheduleCallbackForTarget(_this, function() {cc.audioEngine.stopEffect(sid);}, 1, 0, 0, false);
			}
		}

		//move a piece
		var row=9-parseInt(string[2]);
		var col=parseInt(string[3]);
		var placed = false;
		if (row>=0 && row<_this.chess_board.board_height && col>=0 && col<_this.chess_board.board_width) {
			var last_row = _this.selected_piece.last_board_position.row;
			var last_col = _this.selected_piece.last_board_position.col;
			if (last_row != row || last_col !=col) {
				if (_this.is_valid_move(row, col)) {
					var enemy_piece = _this.chess_board.board_map[row][col];
					if (enemy_piece != null) {
						_this.capture_piece(enemy_piece);
					}
					_this.selected_piece.setPosition(_this.chess_board.get_point_at(row, col));
					console.log(row);
					console.log(col);
								
					_this.set_board_map(_this.selected_piece, row, col);
					
					_this.set_board_map(null, last_row, last_col);			
					_this.selected_piece.set_board_position(row, col);
					
					placed = true;
					_this.current_side = _this.current_side == "red" ? "black" : "red";
					_this.clock_layer.pause_time();
					var sid = cc.audioEngine.playEffect(res.ChessMove_mp3);
					cc.director.getScheduler().scheduleCallbackForTarget(_this, function() {cc.audioEngine.stopEffect(sid);}, 1, 0, 0, false);
					//cc.audioEngine.stopEffect(sid);
					if (enemy_piece!=null) {
						if (enemy_piece.piece_type == "king") {
							_this.hud_layer.visible = true;
							_this.clock_layer.reset_clock();
							_this.game_running = false;
						}
					}
				}
			}												
		}
		if (!placed) {
			_this.selected_piece.go_last_position();
		}
		_this.selected_piece.setScale(1);
		_this.selected_piece.setLocalZOrder(5);		
		_this.selected_piece = null;
		_this.clear_highlight();

		});
		// sleep(1000);
	},
	is_valid_move: function(row, col) {
		for (var i = 0; i < this.possible_move.length; i++) {
			if (row == this.possible_move[i][0] && col == this.possible_move[i][1]) {
				return true;
			}
		}
		return false;
	},
	get_clicked_piece: function(point) {
		if (!this.game_running) {
			return null;
		}
		for (var i=0; i<this.chess_pieces.length; i++) {
			if (this.chess_pieces[i].is_clicked(point)) {
				return this.chess_pieces[i];
			}
		}
		return null;
	},
	capture_piece: function(piece) {
		var captured_pieces = this.down_captured_pieces;
		var down = true;
		if (piece.color != this.down_side) {
			captured_pieces = this.up_captured_pieces;
			down = false;
		}
		if (down) {
			piece.setPosition(25+30*captured_pieces.length, 25);			
		}
		else {
			piece.setPosition(25+30*captured_pieces.length, this.height-25);
		}
		captured_pieces.push(piece);
		var sid = cc.audioEngine.playEffect(res.ChessThrow_mp3);
		cc.director.getScheduler().scheduleCallbackForTarget(this, function() {cc.audioEngine.stopEffect(sid);}, 1, 0, 0, false);
		var i = this.chess_pieces.indexOf(piece);
		if (i >= 0) {
			this.chess_pieces.splice(i, 1);
		}		
	},
	init_piece : function(down_side) {
		if (!down_side) {
			down_side = "red";
		}
		var up_side = "black";
		if (down_side == "black") {
			up_side = "red";
		}
		this.down_side = down_side;
		this.chess_board.down_side = down_side;
		//place down side
		//pawn		
		
		var positions = [
			{
				name: "pawn",
				positions: [[3, 0], [3, 2], [3, 4], [3, 6], [3, 8]]
			},
			{
				name: "cannon",
				positions: [[2, 1], [2, 7]]
			},
			{
				name: "chariot",
				positions: [[0, 0], [0, 8]]
			},
			{
				name: "knight",
				positions: [[0, 1], [0, 7]]
			},
			{
				name: "elephant",
				positions: [[0, 2], [0, 6]]
			},
			{
				name: "guard",
				positions: [[0, 3], [0, 5]]
			},
			{
				name: "king",
				positions: [[0, 4]]
			}
		];
		
		var i = 0, j = 0;
		for (i=0; i<positions.length; i++) {
			var position = positions[i];
			var name = position.name;			
			for (j=0; j<position.positions.length; j++) {
				var row = position.positions[j][0];
				var col = position.positions[j][1];
				var pos = this.chess_board.get_point_at(position.positions[j][0], position.positions[j][1]);
				var chess_piece = new ChessPiece(down_side+'_'+name);
				chess_piece.setPosition(pos);
				chess_piece.set_board_position(row, col);
				
				this.set_board_map(chess_piece, row, col);
				this.addChild(chess_piece);
				this.chess_pieces.push(chess_piece);				
			}
		}
		
		for (i=0; i<positions.length; i++) {
			var position = positions[i];
			var name = position.name;			
			for (j=0; j<position.positions.length; j++) {
				var row = 9 - position.positions[j][0];
				var col = position.positions[j][1];
				
				var pos = this.chess_board.get_point_at(9 - position.positions[j][0], position.positions[j][1]);
				var chess_piece = new ChessPiece(up_side+'_'+name);
				chess_piece.setPosition(pos);
				chess_piece.set_board_position(row, col);
				
				this.set_board_map(chess_piece, row, col);
				this.addChild(chess_piece);
				this.chess_pieces.push(chess_piece);
			}
		}
		this.game_running = true;		
	},
	set_board_map: function(piece, row, col) {
		this.chess_board.board_map[row][col] = piece;
	},
	highlight_move: function(moves) {
		var i = 0;
		for (i = 0; i<moves.length; i++) {
			var row = moves[i][0];
			var col = moves[i][1];
			var highlight = new HighlightPiece();
			highlight.setPosition(this.chess_board.get_point_at(row, col));
			highlight.setLocalZOrder(999);
			this.addChild(highlight);
			this.highlight_points.push(highlight);
		}
	},
	clear_highlight: function() {
		for (var i = 0; i<this.highlight_points.length; i++) {
			this.removeChild(this.highlight_points[i]);
		}
	},
	set_clock_layer: function(clock_layer) {
		this.clock_layer = clock_layer;
	},
	set_hud_layer: function(hud_layer) {
		this.hud_layer = hud_layer;	
	}
});
