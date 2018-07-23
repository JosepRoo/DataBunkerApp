import { Component, OnInit } from '@angular/core';

import { Message, MessageType } from '../classes/message';
import { MessageService } from '../services/messages.service';

@Component({
    moduleId: module.id,
    selector: 'messages',
    templateUrl: 'messages.component.html'
})

export class MessagesComponent {
    messages: Message[] = [];

    constructor(private messageService: MessageService) { }

    ngOnInit() {
        this.messageService.getAlert().subscribe((message: Message) => {
            if (!message) {
                // clear alerts when an empty alert is received
                this.messages = [];
                return;
            }

            // add alert to array
            this.messages.push(message);
        });
    }

    removeAlert(message: Message) {
        this.messages = this.messages.filter(x => x !== message);
    }

    cssClass(message: Message) {
        if (!alert) {
            return;
        }

        // return css class based on alert type
        switch (message.type) {
            case MessageType.Success:
                return 'alert alert-success';
            case MessageType.Error:
                return 'alert alert-danger';
            case MessageType.Info:
                return 'alert alert-info';
            case MessageType.Warning:
                return 'alert alert-warning';
        }
    }
}
