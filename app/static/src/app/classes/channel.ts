import { Brand } from './brand';

// model for Channel Class
export class Channel {

  public name: string;
  public id: number;
  public brands: Brand[];

  constructor(id: number, name: string, brands) {
    var self = this;
    self.name = name;
    self.id = id;
    self.brands = [];
    brands.forEach(function(brand){
      self.brands.push(new Brand(brand.id, brand.name, brand.categories));
    });
  };

  public deleteChildren(){
    this.brands = null;
  }

}
