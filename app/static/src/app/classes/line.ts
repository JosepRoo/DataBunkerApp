import { Channel } from './channel';
import { Brand } from './brand';
import { Category } from './category';
import { Product } from './product';

// model for Line Class
export class Line {

  public channel: Channel;
  public brand: Brand;
  public category: Category;
  public product: Product;
  public color: string;
  public data: object;

  constructor(){}

  public deleteChannel() {
    this.channel = null;
    this.deleteCategory();
  }

  public deleteBrand() {
    this.brand = null;
    this.deleteProduct();
  }

  public deleteCategory() {
    this.category = null;
    this.deleteBrand();
  }

  public deleteProduct() {
    this.product = null;
  }

}
