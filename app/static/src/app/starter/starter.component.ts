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
	data: any[] = [];
	startDate = "2018-01-01";
	endDate = "2018-12-31";

	constructor(
		private messageService: MessageService,
		private channelService: ChannelService,
		private colorGenerator: ColorGeneratorService
	) {
		var self = this;
		this.channelService.getChannels().subscribe(res => {
			self.channels = res;
		}, (err) => {
				if (err === 'Unauthorized'){
				}
		});

	}

	getCategories() {
		var self = this;
		self.line.category = null;
		self.line.brand = null;
		self.line.product = null;
		if (this.line.channel)
			this.channelService.getChannelSubElemenets(this.line.channel._id).subscribe(res => {
				self.line.channel.sub_elements = res;
			}, (err) => {
					if (err === 'Unauthorized'){
					}
			});
	}

	getBrands() {
		var self = this;
		self.line.brand = null;
		self.line.product = null;
		if (this.line.category)
			this.channelService.getCategorySubElemenets(this.line.category._id).subscribe(res => {
				self.line.category.sub_elements = res;
			}, (err) => {
					if (err === 'Unauthorized'){
					}
			});
	}

	getProducts() {
		var self = this;
		self.line.product = null;
		if (this.line.brand)
			this.channelService.getBrandSubElemenets(this.line.brand._id).subscribe(res => {
				self.line.brand.sub_elements = res;
			}, (err) => {
					if (err === 'Unauthorized'){
					}
			});
	}

	// send a message to messages component
	sendMessage(message, type) {
		this.messageService.success(message);
	}

	addLine() {
		this.line.color = this.colorGenerator.getColor();
		this.line.data = {datos: 1000};
		this.lines.push(this.line);
		var data;
		if (this.line.product == null){
			this.channelService.getData("brand", this.line.brand._id, this.startDate, this.endDate).subscribe(res => {
				data = res
			}, (err) => {
					if (err === 'Unauthorized'){
					}
			});
			if (this.line.brand == null){
				this.channelService.getData("category", this.line.category._id, this.startDate, this.endDate).subscribe(res => {
					data = res
				}, (err) => {
						if (err === 'Unauthorized'){
						}
				});
				if (this.line.category == null){
					this.channelService.getData("channel", this.line.channel._id, this.startDate, this.endDate).subscribe(res => {
						data = res
					}, (err) => {
							if (err === 'Unauthorized'){
							}
					});
				}
			}

		} else {
			this.channelService.getData("product", this.line.product._id, this.startDate, this.endDate).subscribe(res => {
				data = res
			}, (err) => {
					if (err === 'Unauthorized'){
					}
			});
		}
		console.log(data);
		if (data){
			this.data.push(data);
		}

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
