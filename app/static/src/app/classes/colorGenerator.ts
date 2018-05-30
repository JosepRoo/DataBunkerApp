// auxiliary class for generating colors
export class ColorGenerator {

  private colors: string[];
  private index: number;

  constructor(){
    this.colors = ['#5c4ac7', '#009efb', '#38b6ba', 'rgb(101, 186, 105)', 'rgb(205, 148, 101)', 'rgb(226, 213, 102)'];
    this.index = 0;
  }

  // return the next color of the sequence
  next(){
    let color = this.colors[this.index];
    this.index++;
    if (this.index >= this.colors.length){
      this.index = 0;
    }
    return color;
  }

}
