import { RouteInfo } from './sidebar.metadata';

export const ROUTES: RouteInfo[] = [
    {
        path: '', title: 'Principal', icon: '', class: 'nav-small-cap', label: '', labelClass: '', extralink: true, submenu: []
    },
    {
        path: '/comparador', title: 'Comparador', icon: 'mdi mdi-gauge', class: '', label: '', labelClass: '', extralink: false, submenu: []
    },
    {
        path: '/products', title: 'Productos', icon: 'mdi mdi-wallet-travel', class: '', label: '', labelClass: '', extralink: false, submenu: []
    }
    // {
    //     path: '', title: 'Menu Levels', icon: 'mdi mdi-arrange-send-backward', class: 'has-arrow', label: '', labelClass: '', extralink: false,
    //     submenu: [
    //         { path: 'javascript:void(0);', title: 'Second Level', icon: '', class: '', label: '', labelClass: '', extralink: true, submenu: [] },
    //         {
    //             path: '', title: 'Second Child', icon: '', class: 'has-arrow', label: '', labelClass: '', extralink: false,
    //             submenu: [
    //                 { path: 'javascript:void(0);', title: 'Third 1.1', icon: '', class: '', label: '', labelClass: '', extralink: false, submenu: [] },
    //                 { path: 'javascript:void(0);', title: 'Third 1.2', icon: '', class: '', label: '', labelClass: '', extralink: false, submenu: [] },
    //             ]
    //         },
    //     ]
    // }

];
