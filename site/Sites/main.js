cc.game.onStart = function(){
    cc.view.setDesignResolutionSize(480, 640, cc.ResolutionPolicy.SHOW_ALL);
	cc.view.resizeWithBrowserSize(true);
    //load resources
    cc.LoaderScene.preload(g_resources, function () {
        cc.director.runScene(new ChessScene());
    }, this);
};
var socket=io.connect()

cc.game.run();
