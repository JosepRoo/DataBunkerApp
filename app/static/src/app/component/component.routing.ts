import { Routes } from '@angular/router';

import { NgbdpregressbarBasic } from './progressbar/progressbar.component';
import { NgbdpaginationBasic } from './pagination/pagination.component';
import { NgbdAccordionBasic } from './accordion/accordion.component';
import { NgbdAlertBasic } from './alert/alert.component';
import { NgbdCarouselBasic } from './carousel/carousel.component';
import { NgbdDatepickerBasic } from './datepicker/datepicker.component';
import { NgbdDropdownBasic } from './dropdown-collapse/dropdown-collapse.component';
import { NgbdModalBasic } from './modal/modal.component';
import { NgbdPopTooltip } from './popover-tooltip/popover-tooltip.component';
import { NgbdratingBasic } from './rating/rating.component';
import { NgbdtabsBasic } from './tabs/tabs.component';
import { NgbdtimepickerBasic } from './timepicker/timepicker.component';
import { NgbdtypeheadBasic } from './typehead/typehead.component';
import { CardsComponent } from './card/card.component';
import { ButtonsComponent } from './buttons/buttons.component';

export const ComponentsRoutes: Routes = [
  {
    path: '',
    children: [
    {
      path: '', redirectTo: 'progressbar', pathMatch: 'full',
    },
    {
      path: 'progressbar',
      component: NgbdpregressbarBasic,
      data: {
        title: 'Progressbar',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Progressbar'}]
      }
    },
    {
      path: 'pagination',
      component: NgbdpaginationBasic,
      data: {
        title: 'Pagination',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Pagination'}]
      }
    },
    {
      path: 'accordion',
      component: NgbdAccordionBasic,
      data: {
        title: 'Accordion',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Accordion'}]
      }
    },
    {
      path: 'alert',
      component: NgbdAlertBasic,
      data: {
        title: 'Alert',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Alert'}]
      }
    },
    {
      path: 'carousel',
      component: NgbdCarouselBasic,
      data: {
        title: 'Carousel',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Carousel'}]
      }
    },
    {
      path: 'datepicker',
      component: NgbdDatepickerBasic,
      data: {
        title: 'Datepicker',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Datepicker'}]
      }
    },
    {
      path: 'dropdown',
      component: NgbdDropdownBasic,
      data: {
        title: 'Dropdown',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Dropdown'}]
      }
    },
    {
      path: 'modal',
      component: NgbdModalBasic,
      data: {
        title: 'Modal',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Modal'}]
      }
    },
    {
      path: 'poptool',
      component: NgbdPopTooltip,
      data: {
        title: 'Popover & Tooltip',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Popover & Tooltip'}]
      }
    },
    {
      path: 'rating',
      component: NgbdratingBasic,
      data: {
        title: 'Rating',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Rating'}]
      }
    },
    {
      path: 'tabs',
      component: NgbdtabsBasic,
      data: {
        title: 'Tabs',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Tabs'}]
      }
    },
    {
      path: 'timepicker',
      component: NgbdtimepickerBasic,
      data: {
        title: 'Timepicker',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Timepicker'}]
      }
    },
    {
      path: 'typehead',
      component: NgbdtypeheadBasic,
      data: {
        title: 'Typehead',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Typehead'}]
      }
    },
    {
      path: 'buttons',
      component: ButtonsComponent,
      data: {
        title: 'Button',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Button'}]
      }
    },
    {
      path: 'cards',
      component: CardsComponent,
      data: {
        title: 'Card',
        urls: [{title: 'Componentes',url: '/component/accordion'},{title: 'ngComponent'},{title: 'Card'}]
      }
    }]
  }
];
