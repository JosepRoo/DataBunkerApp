import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { StarterComponent } from './starter.component';
import { GraphComponent } from './graph/graph.component';

// charts
import * as FusionCharts from 'fusioncharts';
import * as Charts from 'fusioncharts/fusioncharts.charts';
import * as FintTheme from 'fusioncharts/themes/fusioncharts.theme.fint';
import { FusionChartsModule } from 'angular4-fusioncharts';
import { AmChartsModule } from "@amcharts/amcharts3-angular";

const routes: Routes = [{
	path: '',
	data: {
        title: 'Principal',
        urls: [{title: 'Principal', url: '/dashboard'}, {title: 'Comparador'}]
    },
	component: StarterComponent
}];

@NgModule({
	imports: [
    	FormsModule,
    	CommonModule,
    	RouterModule.forChild(routes),
			FusionChartsModule.forRoot(FusionCharts, Charts, FintTheme),
			AmChartsModule
    ],
	declarations: [StarterComponent, GraphComponent]
})
export class StarterModule { }
