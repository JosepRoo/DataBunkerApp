

// model for Privilege Class
export class Privilege {

  private id: Number;
  private name: String;
  private children: Privilege[];
  private usable: Boolean;
  private type: String;

  // initialize the object Filter
  constructor(id: Number, name: String, children: Privilege[], usable: Boolean, type:String){
    this.id = id;
    this.name = name;
    this.children = children;
    this.type = type;
  }

  // return the id of this Filter
  public getId(){
    return this.id;
  }

  // return the anme of this Filter
  public getName(){
    return this.name;
  }

  // return the children of this Filter
  public getChildren(){
    return this.children;
  }

  // return the usable of this Filter
  public getUsable(){
    return this.usable;
  }

  // set the id to the one received
  public setId(id){
    this.id = id;
  }

  // set the name to the one received
  public sentName(name){
    this.name = name;
  }

  // set the children to the one received
  public setChildren(children){
    this.children = children;
  }

  // set the usable to the one received
  public setUsable(usable){
    this.usable = usable;
  }

}
