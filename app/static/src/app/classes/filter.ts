import { Privilege } from "../classes/privilege";


// model for Filter Class
export class Filter {

  private brand: Privilege;
  private category: Privilege;
  private product: Privilege;
  private priceRange: string;

  // initialize the object Filter
  constructor(brand: Privilege, category: Privilege, product: Privilege, priceRange: string){
    this.brand = brand;
    this.category = category;
    this.product = product;
    this.priceRange = priceRange;
  }

  // return the brand of this Filter
  public getBrand(){
    return this.brand;
  }

  // return the category of this Filter
  public getCategory(){
    return this.category;
  }

  // return the product of this Filter
  public getProduct(){
    return this.product;
  }

  // return the priceRange of this Filter
  public getPriceRange(){
    return this.priceRange;
  }

  // set the brand tothe one received
  public setBrand(brand){
    this.brand = brand;
  }

  // set the category tothe one received
  public setCategory(category){
    this.category = category;
  }

  // set the product tothe one received
  public setProduct(product){
    this.product = product;
  }

  // set the priceRange tothe one received
  public setPriceRange(priceRange){
    this.priceRange = priceRange;
  }

  // print the object
  public print(){
    console.log("Filter: ", JSON.stringify(this));
  }

}
