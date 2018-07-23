import { Brand } from './brand';

// model for Category Class
export class Category {

  public name: string;
  public _id: string;
  public sub_elements: Brand[] | null;

}
