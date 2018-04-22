import { Component, AfterViewInit } from '@angular/core';

// Services
import { MessageService } from '../services/messages.service';
import { ChannelService } from '../services/channels.service';
import { ColorGeneratorService } from '../services/colorGenerator.service';

// classes
import { Line } from '../classes/line';
import { Channel } from '../classes/channel';
// import { ColorGenerator } from '../classes/colorGenerator';

@Component({
	templateUrl: './starter.component.html',
	styleUrls: ['./starter.component.css']

})

export class StarterComponent implements AfterViewInit {

	channels: Channel[];
	line = new Line();
	lines: Line[] = [];

	constructor(
		private messageService: MessageService,
		private channelService: ChannelService,
		private colorGenerator: ColorGeneratorService
	) {
		this.channels = channelService.getChannels();
	}

	// send a message to messages component
	sendMessage(message, type) {
		this.messageService.success(message);
	}

	addLine() {
		this.line.color = this.colorGenerator.getColor();
		this.line.data = {datos: 1000};
		this.lines.push(this.line);
		this.line = new Line();
	}

	removeLine(line: Line){
		var index = this.lines.indexOf(line);
		if (index > -1) {
		   this.lines.splice(index, 1);
		}
	}

	ngAfterViewInit() {

	}

}
