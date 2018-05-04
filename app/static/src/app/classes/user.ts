// model for User Class
import { Company } from "../classes/company";

export class User {
    _id: string;
    name: string;
    email: string;
    password: string;
    privileges: any;
    // company: Company;
}
