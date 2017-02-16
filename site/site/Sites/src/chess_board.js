var BoardLayer = cc.Layer.extend({
	chess_board : null,
	ctor : function() {
		this._super();
	},
	init : function() {
		this._super();
		var winsize = cc.director.getWinSize();
		var centerpos = cc.p(winsize.width / 2, winsize.height / 2);

		var spritebg = cc.Sprite.create(res.ChessBoardBackground_png);
		spritebg.setScale(winsize.width / spritebg.width);
		spritebg.setPosition(centerpos);
		this.addChild(spritebg);

		var board = new ChessBoard();
		board.setPosition((winsize.width - board.width) / 2, (winsize.height - board.height) / 2);
		board.init_board();
		this.addChild(board);
		this.chess_board = board;
	}
});

var ChessBoard = cc.DrawNode.extend({
	points : [],
	point_distance : 50,
	board_width : 9,
	board_height : 10,
	board_map: [],
	down_side: "red",
	ctor : function() {
		this._super();
		var winsize = cc.director.getWinSize();
		this.point_distance = winsize.width / 9;
		this.width = (this.board_width - 1) * this.point_distance;
		this.height = (this.board_height - 1) * this.point_distance;
		this.init_board();
	},
	init_board : function() {
		this.board_map = [];
		this.points = [];
		var width = this.board_width;
		var height = this.board_height;
		var point_distance = this.point_distance;
		var i = 0, j = 0;
		var line = [];
		var line_map = [];
		for ( i = 0; i < height; i++) {
			line = [];
			line_map = [];
			for ( j = 0; j < width; j++) {
				var point = new cc.Point(j * point_distance, i * point_distance);
				line.push(point);
				line_map.push(null);
			}
			this.points.push(line);
			this.board_map.push(line_map);
		}
		this.draw_board();
	},
	draw_board : function() {
		var width = this.board_width;
		var height = this.board_height;
		var line_width = 3;
		var point_radius = 2;
		var alpha = 0xff;
		var color = new cc.Color(0, 0, 0, alpha);
		var i = 0, j = 0;
		var all_dots = [];
		for ( i = 0; i < height; i++) {
			this.drawSegment(this.points[i][0], this.points[i][8], line_width, color);
		}
		this.drawSegment(this.points[0][0], this.points[9][0], line_width, color);
		this.drawSegment(this.points[0][8], this.points[9][8], line_width, color);
		for ( i = 1; i < width - 1; i++) {
			this.drawSegment(this.points[0][i], this.points[4][i], line_width, color);
			this.drawSegment(this.points[5][i], this.points[9][i], line_width, color);
		}
		//draw crosses
		this.drawSegment(this.points[0][3], this.points[2][5], line_width, color);
		this.drawSegment(this.points[2][3], this.points[0][5], line_width, color);

		this.drawSegment(this.points[9][3], this.points[7][5], line_width, color);
		this.drawSegment(this.points[7][3], this.points[9][5], line_width, color);
	},
	get_point_at : function(row, col) {
		return this.convertToWorldSpace(this.points[row][col]);
	},
	get_possible_move: function(row, col) {
		var piece = this.board_map[row][col];		
		var result = [];
		var i = 0, j = 0;
		if (piece == null) {
			return [];
		}
		var _this = this;
		console.log("possible");
		function correct_result() {
			/*
			 * remove outbound and ally result
			 */
			var result_2 = [];
			for (i = 0; i<result.length; i++) {
				var row = result[i][0];
				var col = result[i][1];
				if (row < 0 || row >= _this.board_height || col < 0 || col >= _this.board_width) {
					continue;
				}
				if (_this.board_map[row][col] != null) {
					if (_this.board_map[row][col].color == piece.color) {
						continue;
					}
				}
				result_2.push(result[i]);
			}
			return result_2;
		}
		switch (piece.piece_type) {
			case "pawn":
				if (this.down_side == piece.color) {					
					result.push([row + 1, col]);					
					if (row > 4) {
						result = result.concat([[row, col + 1], [row, col - 1]]);	
					}
				}
				else {
					result.push([row - 1, col]);
					if (row < 5) {
						result = result.concat([[row, col + 1], [row, col - 1]]);	
					}
				}
				result = correct_result();
				break;
			case "cannon":
				for (i = row + 1; i < this.board_height; i++) {
					if (this.board_map[i][col] == null) {
						result.push([i, col]);
					}
					else {
						for (j=i+1; j < this.board_height; j++) {
							if (this.board_map[j][col] != null) {
								if (this.board_map[j][col].color != piece.color) {
									result.push([j, col]);
									break;
								}
							}
						}
						break;
					}
				}
				for (i = row - 1; i >= 0; i--) {
					if (this.board_map[i][col] == null) {
						result.push([i, col]);
					}
					else {
						for (j=i-1; j >= 0; j--) {
							if (this.board_map[j][col] != null) {
								if (this.board_map[j][col].color != piece.color) {
									result.push([j, col]);
									break;
								}
							}
						}
						break;
					}
				}
				for (i = col + 1; i < this.board_width; i++) {
					if (this.board_map[row][i] == null) {
						result.push([row, i]);
					}
					else {
						for (j=i+1; j < this.board_width; j++) {
							if (this.board_map[row][j] != null) {
								if (this.board_map[row][j].color != piece.color) {
									result.push([row, j]);
									break;
								}
							}
						}
						break;
					}
				}
				for (i = col - 1; i >= 0; i--) {
					if (this.board_map[row][i] == null) {
						result.push([row, i]);
					}
					else {
						for (j=i-1; j >= 0; j--) {
							if (this.board_map[row][j] != null) {
								if (this.board_map[row][j].color != piece.color) {
									result.push([row, j]);
									break;
								}
							}
						}
						break;
					}
				}
				break;
			case "chariot":
				for (i = row + 1; i < this.board_height; i++) {
					if (this.board_map[i][col] == null) {
						result.push([i, col]);
					}
					else {
						if (this.board_map[i][col].color != piece.color) {
							result.push([i, col]);
						}
						break;
					}
				}
				for (i = row - 1; i >= 0; i--) {
					if (this.board_map[i][col] == null) {
						result.push([i, col]);
					}
					else {
						if (this.board_map[i][col].color != piece.color) {
							result.push([i, col]);
						}
						break;
					}
				}
				for (i = col + 1; i < this.board_width; i++) {
					if (this.board_map[row][i] == null) {
						result.push([row, i]);
					}
					else {
						if (this.board_map[row][i].color != piece.color) {
							result.push([row, i]);
						}
						break;
					}
				}
				for (i = col - 1; i >= 0; i--) {
					if (this.board_map[row][i] == null) {
						result.push([row, i]);
					}
					else {
						if (this.board_map[row][i].color != piece.color) {
							result.push([row, i]);
						}
						break;
					}
				}
				break;
			
			case "knight":
				var _r = [];
				if (col+1 < this.board_width) {
					if (this.board_map[row][col+1] == null) {
						_r.push([row+1, col+2],[row-1, col+2]);
					}
				}
				if (col-1 >= 0) {
					if (this.board_map[row][col-1] == null) {
						_r.push([row+1, col-2],[row-1, col-2]);
					}
				}			
				if (row + 1 < this.board_height) {
					if (this.board_map[row+1][col] == null) {
						_r.push([row+2, col+1], [row+2, col-1]);
					}
				}
				if (row - 1 >= 0) {
					if (this.board_map[row-1][col] == null) {
						_r.push([row-2, col+1], [row-2, col-1]);
					}
				}	
				result = result.concat(_r);
				result = correct_result();
				break;
			
			case "elephant":
				var _r = [];
				
				if (row+1 < this.board_height && col+1 < this.board_width) {
					if (this.board_map[row+1][col+1] == null) {
						_r.push([row+2, col+2]);
					}
				}
				if (row+1 < this.board_height && col-1 >= 0) {
					if (this.board_map[row+1][col-1] == null) {
						_r.push([row+2, col-2]);
					}
				}
				if (row-1 >=0 && col+1 < this.board_width) {
					if (this.board_map[row-1][col+1] == null) {
						_r.push([row-2, col+2]);
					}
				}
				
				if (row-1 >=0 && col-1 >= 0) {
					if (this.board_map[row-1][col-1] == null) {
						_r.push([row-2, col-2]);
					}
				}
				var _rr = [];
				for (i = 0; i<_r.length; i++) {
					var _row = _r[i][0];
					if (this.down_side == piece.color) {						
						if (_row < 5) {
							_rr.push(_r[i]);
						}
					}
					else {
						if (_row >= 5) {
							_rr.push(_r[i]);
						}
					}
				}
				
				result = result.concat(_rr);
				result = correct_result();
				break;
				
			case "guard":
				var _r = [
						[row+1, col+1],
						[row+1, col-1],
						[row-1, col+1],
						[row-1, col-1]
					];				
				var _rr = [];
				for (i = 0; i<_r.length; i++) {
					var _row = _r[i][0];
					var _col = _r[i][1];
					if (this.down_side == piece.color) {
						if (_row >= 0 && _row <=2 && _col>=3 && _col<=5) {
							_rr.push(_r[i]);
						}
					}
					else {
						if (_row >= 7 && _row <=9 && _col>=3 && _col<=5) {
							_rr.push(_r[i]);
						}
					}
				}
				result = result.concat(_rr);
				result = correct_result();
				break;
				
			case "king":
				if (this.down_side == piece.color) {
					var _r = [
							[row+1, col],
							[row, col+1],
							[row-1, col],
							[row, col-1],
							[7, col],
							[8, col],
							[9, col]
						];			
				}
				else{
					var _r = [
							[row+1, col],
							[row, col+1],
							[row-1, col],
							[row, col-1],
							[0, col],
							[1, col],
							[2, col]
						];	
				}	
				var _rr = [];
				console.log("king");
				for (i = 0; i<_r.length; i++) {
					var _row = _r[i][0];
					var _col = _r[i][1];
					if (this.down_side == piece.color) {
						if (_row >= 0 && _row <=2 && _col>=3 && _col<=5) {
							_rr.push(_r[i]);
						}
						else if (_row > 6){
							temp_p = this.board_map[_row][_col];
							if (temp_p != null){
								if (temp_p.piece_type == "king"){
									var flag = 0;
									for (var j = row+1; j < _row; j++) {
										if (this.board_map[j][_col] != null){
											flag = 1;
											break;
										}
									}
									if (flag == 0){
										_rr.push(_r[i]);
									}
								}
							}
						}
					}
					else {
						if (_row >= 7 && _row <=9 && _col>=3 && _col<=5) {
							_rr.push(_r[i]);
						}
						else if (_row < 3){
							temp_p = this.board_map[_row][_col];
							if (temp_p != null){
								if (temp_p.piece_type == "king"){
									var flag = 0;
									for (var j = _row+1; j < row; j++) {
										if (this.board_map[j][_col] != null){
											flag = 1;
											break;
										}
									}
									if (flag == 0){
										_rr.push(_r[i]);
									}
								}
							}
						}
					}
				}
				result = result.concat(_rr);
				result = correct_result();
				break;
			
			default:
				result = [];			
		}
		return result;
	}
});