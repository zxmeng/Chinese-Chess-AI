var ChessScene = cc.Scene.extend({
	ctor: function() {
		this._super();
	},
	onEnter : function() {
		this._super();
		var started = false;
		cc.spriteFrameCache.addSpriteFrames(res.ChessPieces_plist);
		
		var colorlayer = new cc.LayerColor();
		var color = new cc.Color(0xf1, 0xcb, 0x9d, 0xff);
		colorlayer.setColor(color);
		var board_layer = new BoardLayer();
		board_layer.init();
		var piece_layer = new PieceLayer(board_layer.chess_board);
		var clock_layer = new ChessClockLayer();
		piece_layer.set_clock_layer(clock_layer);
		
		var down_side = "red";				
		var play_callback = function() {
			if (!started) {
				clock_layer.start_time("down");					
				started = true;
			}
			else {			
				down_side = down_side == "red" ? "black" : "red";
				piece_layer.reset_piece();
				if (down_side == "red") {
					clock_layer.start_time("down");
				}
				else {
					clock_layer.start_time("up");
				}
							
			}
			this.visible = false;
		};
		var hud_layer = new ChessHUDLayer(play_callback);
		piece_layer.set_hud_layer(hud_layer);
		this.addChild(colorlayer);
		this.addChild(board_layer);
		this.addChild(piece_layer);								
		this.addChild(clock_layer);
		this.addChild(hud_layer);
		piece_layer.init_piece(down_side);
		console.log("start");
	}
});

