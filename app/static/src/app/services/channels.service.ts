import { Injectable } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

import { Channel } from '../classes/channel';

import { catchError, map, tap } from 'rxjs/operators';

@Injectable()
export class ChannelService {


  private channelUrl = 'api/channel';

  getChannels(): Channel[] {
    let channels: Channel[] = [];
    let json = [
    	{
    		name: 'Amazon',
    		id: 1,
    		brands: [
    			{
    				name: 'RayBan',
    				id: 1,
    				categories: [
    					{
    						name: "Sunglasses",
    						id: 1,
    						products: [
    							{
    								name: "Aviator",
    								id: 1
    							},
    							{
    								name: "Longth",
    								id: 2
    							},
    							{
    								name: "Sepia",
    								id: 3
    							}
    						]
    					},
    					{
    						name: "Glasses",
    						id: 1,
    						products: [
    							{
    								name: "Aviator",
    								id: 1
    							},
    							{
    								name: "Longth",
    								id: 2
    							},
    							{
    								name: "Sepia",
    								id: 3
    							}
    						]
    					},
    					{
    						name: "Clothes",
    						id: 1,
    						products: [
    							{
    								name: "T-Shirt",
    								id: 1
    							},
    							{
    								name: "Pants",
    								id: 2
    							},
    							{
    								name: "Jeans",
    								id: 3
    							}
    						]
    					}
    				]
    			},
    			{
    				name: 'Polo',
    				id: 1,
    				categories: [
    					{
    						name: "Accesories",
    						id: 1,
    						products: [
    							{
    								name: "Belt",
    								id: 1
    							},
    							{
    								name: "Sunglasses",
    								id: 2
    							},
    							{
    								name: "Wallets",
    								id: 3
    							}
    						]
    					},
    					{
    						name: "Shirts",
    						id: 1,
    						products: [
    							{
    								name: "Polo",
    								id: 1
    							},
    							{
    								name: "Turtle",
    								id: 2
    							},
    							{
    								name: "Formal",
    								id: 3
    							}
    						]
    					},
    					{
    						name: "Jeans",
    						id: 1,
    						products: [
    							{
    								name: "Short",
    								id: 1
    							},
    							{
    								name: "Long",
    								id: 2
    							},
    							{
    								name: "Retro",
    								id: 3
    							}
    						]
    					}
    				]
    			}
    		]
    	}
    ];
    json.forEach(function(channel){
      channels.push(new Channel(channel.id, channel.name, channel.brands))
    })
    return channels;
  }

}
