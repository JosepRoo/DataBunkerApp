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

  constructor(){}

  public deleteChannel() {
    this.channel = null;
    this.deleteBrand();
  }

  public deleteBrand() {
    this.brand = null;
    this.deleteCategory();
  }

  public deleteCategory() {
    this.category = null;
    this.deleteProduct();
  }

  public deleteProduct() {
    this.product = null;
  }

}
