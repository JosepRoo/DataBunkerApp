// model for Message Class
export class Message {
    type: MessageType;
    message: string;
}

// model for Message Type enum
export enum MessageType {
    Success,
    Error,
    Info,
    Warning
}
