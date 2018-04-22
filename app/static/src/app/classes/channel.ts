import { Category } from './category';

// model for Channel Class
export class Channel {

  public name: string;
  public id: number;
  public categories: Category[];

  constructor(id: number, name: string, categories) {
    var self = this;
    self.name = name;
    self.id = id;
    self.categories = [];
    categories.forEach(function(category){
      self.categories.push(new Category(category.id, category.name, category.brands));
    });
  };

  public deleteChildren(){
    this.categories = null;
  }

}
