
// model for Product Class
export class Product {

  public name: string;
  public id: number;

  constructor(id: number, name: string ){
    this.id = id;
    this.name = name;
  };

  public deleteChildren(){
    console.log("No more children");
  }

}
