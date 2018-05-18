import { Component, AfterViewInit, ViewChild } from '@angular/core';

// Services
import { MessageService } from '../services/messages.service';
import { ChannelService } from '../services/channels.service';
import { ColorGeneratorService } from '../services/colorGenerator.service';

import { GraphComponent } from './graph/graph.component';

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
	chartData: any[] = [];
	startDate : Date = new Date();
	endDate: Date = new Date();

	@ViewChild(GraphComponent) child: GraphComponent;

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

		this.startDate.setDate(this.endDate.getDate()-30);
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
		var self = this;
		if (this.line.category == null){
			this.line.name = this.line.channel.name;
			this.channelService.getData("channel", this.line.channel._id, this.startDate, this.endDate).subscribe(res => {
				self.line.data = res;
				self.data.push(res);
				self.line.color = self.colorGenerator.getColor();
				self.lines.push(self.line);
				self.chartData = self.generateData();
				self.line = new Line();
			}, (err) => {
					if (err === 'Unauthorized'){
					}
			});
		} else {
			if (this.line.brand == null){
				this.line.name = this.line.category.name;
				this.channelService.getData("category", this.line.category._id, this.startDate, this.endDate).subscribe(res => {
					self.line.data = res;
					self.data.push(res);
					self.line.color = self.colorGenerator.getColor();
					self.lines.push(self.line);
					self.chartData = self.generateData();
					self.line = new Line();
				}, (err) => {
						if (err === 'Unauthorized'){
						}
				});
			} else {
				if (this.line.product == null){
					this.line.name = this.line.brand.name;
					this.channelService.getData("brand", this.line.brand._id, this.startDate, this.endDate).subscribe(res => {
						self.line.data = res;
						self.data.push(res);
						self.line.color = self.colorGenerator.getColor();
						self.lines.push(self.line);
						self.chartData = self.generateData();
						self.line = new Line();
					}, (err) => {
							if (err === 'Unauthorized'){
							}
					});
				} else {
					this.line.name = this.line.product.name;
					this.channelService.getData("product", this.line.product._id, this.startDate, this.endDate).subscribe(res => {
						self.line.data = res;
						self.data.push(res);
						self.line.color = self.colorGenerator.getColor();
						self.lines.push(self.line);
						self.chartData = self.generateData();
						self.line = new Line();
					}, (err) => {
							if (err === 'Unauthorized'){
							}
					});
				}
			}
		}
	}

	generateData(): any[]{
		var diff = Math.abs(this.startDate.getTime() - this.endDate.getTime());
		var diffDays = Math.ceil(diff / (1000 * 3600 * 24));
		var date = new Date(this.startDate.getTime());
		var axisX = [];
		var chartData = [];
		for (var i = 0; i < diffDays; i ++){

			date.setDate(date.getDate()+ 1);
			var dateString = date.getFullYear() + '/' + ("0" + (date.getMonth() + 1)).slice(-2) + '/' +("0" + (date.getDate())).slice(-2);
			axisX.push(dateString);
		}
		var day;
		for(var i = 0; i < axisX.length; i++){
			day = axisX[i];
			var defDate = new Date(day);
			chartData.push({
				date: defDate
			})
			for (var e = 0; e < this.lines.length; e ++){
				var line = this.lines[e];
				for (var h = 0; h < line.data.length; h ++){
					var dat = line.data[h];
					if (dat._id == day){
						chartData[i][line.name] = Math.round(dat.average * 100) / 100;
					}
				}
			}

		}
		return chartData;
	}

	removeLine(line: Line){
		var index = this.lines.indexOf(line);
		if (index > -1) {
			var name = this.lines[index].name;
			for (var i = 0; i< this.chartData.length; i++){
				delete this.chartData[i][name];
			}
		   this.lines.splice(index, 1);
		}
		this.child.ngAfterViewInit();
	}

	ngAfterViewInit() {

	}

	getScope(line) {
		console.log(line.data);
		try{
			return (line.data[line.data.length-2].average - line.data[line.data.length-1].average)*100/line.data[line.data.length-1].average;
		} catch(e){
			return 0;
		}

	}



}
