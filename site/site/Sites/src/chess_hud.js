var ChessHUDLayer = cc.LayerColor.extend({
	startGameCallback: null,
	ctor: function(startGameCallback) {
		this._super();
		var color = cc.color(0, 255, 0, 100);
		this.setColor(color);
		var winsize = cc.director.getWinSize();
		var sprite1 = new cc.Sprite(res.ButtonPlay_png);
		var sprite2 = new cc.Sprite(res.ButtonPlayS_png);
		var menuItemRestart = cc.MenuItemSprite.create(sprite1, sprite2, startGameCallback, this);			
		
		var menu = cc.Menu.create(menuItemRestart);
		menu.setOpacity(180);        
		var centerpos = cc.p(winsize.width/2, winsize.height/2);				
		menu.setPosition(centerpos);
		this.addChild(menu);
	},
    startGame: function() {
    	this.visible = false;
    	console.log("start game");
    }
});
