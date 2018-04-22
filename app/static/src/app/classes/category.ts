import { Brand } from './brand';

// model for Category Class
export class Category {

  public name: string;
  public id: number;
  public brands: Brand[];

  constructor(id: number, name:string, brands){
    var self = this;
    self.name = name;
    self.id = id;
    self.brands = [];
    brands.forEach(function(brand){
      self.brands.push(new Brand(brand.id, brand.name, brand.products));
    });
  };

  public deleteChildren(){
    this.brands = null;
  }

}
