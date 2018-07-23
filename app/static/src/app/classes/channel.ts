import { Category } from './category';

// model for Channel Class
export class Channel {

  public name: string;
  public _id: string;
  public sub_elements: Category[] | null;

}
