import { Product } from './product';

// model for Brand Class
export class Brand {

  public name: string;
  public id: number;
  public products: Product[];

  constructor(id: number, name: string, products){
    var self = this;
    self.name = name;
    self.id = id;
    self.products = [];
    products.forEach(function(product){
      self.products.push(new Product(product.id, product.name));
    });
  };

  public deleteChildren(){
    this.products = null;
  };

}
