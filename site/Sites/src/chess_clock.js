var padded_number = function(number) {
	var s = number.toString();
	return (s.length>=2 ? s : "0"+s);
};

var ChessClockLayer = cc.Layer.extend({
	down_label: null,
	up_label: null,
	current_label: null,
	ctor: function() {
		this._super();
	},
	init: function() {
		this._super();
		var winsize = cc.director.getWinSize();
		var color = cc.color(255,0,0, 255);
		
		var label = cc.LabelTTF.create("00:00:00", "FreeMono", 40);
		label.setColor(color);
		label.setPosition(cc.p(winsize.width - 80, 20));
		label.startTime = new Date();
		label.elapsedTime = 0;		
		this.down_label = label;
		
		var label2 = cc.LabelTTF.create("00:00:00", "FreeMono", 40);
		label2.setColor(color);
		label2.setPosition(cc.p(winsize.width - 80, winsize.height - 30));
		label2.startTime = new Date();	
		label2.elapsedTime = 0;		
		this.up_label = label2;												
		
		this.addChild(label);
		this.addChild(label2);						
	},
	reset_clock: function() {
		cc.director.getScheduler().pauseTarget(this.down_label);
		cc.director.getScheduler().pauseTarget(this.up_label);
		
		this.down_label.setString("00:00:00");
		this.down_label.startTime = new Date();
		this.down_label.elapsedTime = 0;
		
		this.up_label.setString("00:00:00");
		this.up_label.startTime = new Date();
		this.up_label.elapsedTime = 0;
	},
	onEnter: function() {
		this.init();
		cc.director.getScheduler().scheduleCallbackForTarget(this.down_label, this.update_time, 1, cc.REPEAT_FOREVER, 0, true);	
		cc.director.getScheduler().scheduleCallbackForTarget(this.up_label, this.update_time, 1, cc.REPEAT_FOREVER, 0, true);	
			
	},
	update_time: function(delta) {
		var milliseconds = new Date().getTime();
		var delta2 = Math.round((this.elapsedTime + milliseconds - this.startTime.getTime()) / 1000);
		var hour = Math.floor(delta2 / 3600);
		var minute = Math.floor((delta2 % 3600)/60);
		var second = delta2 - minute * 60 - hour*3600;
		this.setString(padded_number(hour) + ':' + padded_number(minute) + ':' + padded_number(second));
	},	
	start_time: function(side) {
		var label = null;
		label = (side == "up" ? this.up_label : this.down_label);
		//console.log(label);
		label.startTime = new Date();
		this.current_label = label;		
		cc.director.getScheduler().resumeTarget(this.current_label);
	},
	pause_time: function() {
		var pause_label = this.current_label;
		//console.log(this.current_label);
		var current_time = new Date();
		pause_label.elapsedTime += current_time.getTime() - pause_label.startTime.getTime();
		var run_label = this.current_label == this.up_label ? this.down_label : this.up_label;		
		run_label.startTime = new Date();
		cc.director.getScheduler().resumeTarget(run_label);
		cc.director.getScheduler().pauseTarget(pause_label);
		this.current_label = run_label;
	}
});
