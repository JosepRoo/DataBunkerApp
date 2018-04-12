import { Component, AfterViewInit } from '@angular/core';

// Services
import { MessageService } from '../services/messages.service';
import { ChannelService } from '../services/channels.service';

// classes
import { Line } from '../classes/line';
import { Channel } from '../classes/channel';

@Component({
	templateUrl: './starter.component.html',
	styleUrls: ['./starter.component.css']

})

export class StarterComponent implements AfterViewInit {

	channels: Channel[];
	line = new Line();

	constructor(
		private messageService: MessageService,
		private channelService: ChannelService
	) {
		this.channels = channelService.getChannels();
	}

	// send a message to messages component
	sendMessage(message, type) {
		this.messageService.success(message);
	}

	addLine() {
		console.log(this.line);
	}

	ngAfterViewInit() {

	}

}
